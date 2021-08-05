import os
from datetime import date, datetime, timedelta
from typing import Literal, Optional

import httpx
import itertools
from pydantic import BaseModel
from hetveldje.utils import current_dt


class FieldDay(BaseModel):
    day: Literal[0, 1, 2, 3, 4, 5, 6]
    times: list[str]

    @property
    def day_name(self) -> str:
        return [
            "Maandag",
            "Dinsdag",
            "Woensdag",
            "Donderdag",
            "Vrijdag",
            "Zaterdag",
            "Zondag",
        ][self.day]

    @property
    def times_str(self) -> str:
        return " | ".join(self.times)

    @property
    def today_times(self) -> list[datetime]:
        today = date.today()
        if self.day != today.weekday():
            return []
        tuples = (
            (int(h), int(m)) for h, _, m in (x.partition(":") for x in self.times)
        )
        deltas = (timedelta(hours=h, minutes=m) for h, m in tuples)
        return [datetime(today.year, today.month, today.day) + dt for dt in deltas]


class Dog(BaseModel):
    dog_name: str
    dog_type: str
    owner_name: str
    picture: str
    gender: Literal["M", "F"]
    extra: list[str]
    dob: date
    times: list[FieldDay]

    @classmethod
    def from_result(cls, data: dict) -> "Dog":
        times_data = {k: v for k, v in data.items() if k.startswith("times_")}
        times = [
            FieldDay(
                day=int(key.rpartition("_")[2]),
                times=[x.strip() for x in value.split(",")],
            )
            for key, value in times_data.items()
        ]
        gender = "M" if data["gender"]["value"] == "Mannetje" else "F"
        dob = date.fromisoformat(data["dob"])
        return cls(
            dog_name=data["dog_name"],
            owner_name=data["owner_name"],
            dog_type=data["dog_type"],
            gender=gender,
            picture=data["picture_url"],
            dob=dob,
            extra=[x.strip() for x in data["extra"].split("\n") if x],
            times=times,
        )

    @classmethod
    def from_api(cls) -> list["Dog"]:
        res = httpx.get(
            "https://api.baserow.io/api/database/rows/table/26193/?user_field_names=true",
            headers={"Authorization": f"Token {os.environ['BASEROW_API_KEY']}"},
        ).json()
        return [cls.from_result(r) for r in res["results"]]

    @property
    def today_times(self) -> list[datetime]:
        return list(itertools.chain(*[x.today_times for x in self.times]))

    @property
    def next_time(self) -> Optional[datetime]:
        now = current_dt().replace(tzinfo=None)
        times = [t for t in self.today_times if t >= now]
        if times:
            return times[0]
        else:
            return None


class HourForecast(BaseModel):
    dt: datetime
    precip_mm: float
    temp_c: float

    @classmethod
    def from_data(cls, data: dict) -> "HourForecast":
        dt = datetime.strptime(data["time"], "%Y-%m-%d %H:%M")
        return cls(dt=dt, temp_c=data["temp_c"], precip_mm=data["precip_mm"])

    @classmethod
    def from_api(cls) -> list["HourForecast"]:
        res = httpx.get(
            f"http://api.weatherapi.com/v1/forecast.json?key={os.environ['WEATHER_API_KEY']}&q=52.073938,5.086407&days=1&aqi=no&alerts=no"
        ).json()
        return [cls.from_data(x) for x in res["forecast"]["forecastday"][0]["hour"]]


class HourData(BaseModel):
    dt: datetime
    dogs: list[Dog]
    forecast: HourForecast

    @property
    def time_fmt(self) -> str:
        return self.dt.strftime("%H:%M")

    @classmethod
    def hour(
        cls, hour: int, forecasts: list[HourForecast], dogs: list[Dog], now: datetime
    ) -> Optional["HourData"]:
        in_range = lambda x: x >= now + timedelta(hours=hour) and x < now + timedelta(
            hours=hour + 1
        )
        forecast = [x for x in forecasts if in_range(x.dt)]
        if not forecast:
            return None
        forecast = forecast[0]
        present = [d for d in dogs if d.next_time and in_range(d.next_time)]
        return cls(dt=now + timedelta(hours=hour), dogs=present, forecast=forecast)

    @classmethod
    def next_5(cls, forecasts: list[HourForecast], dogs: list[Dog]) -> list["HourData"]:
        _now = current_dt().replace(tzinfo=None)
        now = datetime(_now.year, _now.month, _now.day, _now.hour)
        hours = [
            cls.hour(hour=i, forecasts=forecasts, dogs=dogs, now=now)
            for i in range(0, 5)
        ]
        return [x for x in hours if x]

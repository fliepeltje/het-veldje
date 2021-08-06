import httpx
from dataclasses import dataclass
from datetime import datetime
from hetveldje import constants as const
from typing import Optional


@dataclass
class Forecast:
    dt: datetime
    precip_mm: float
    temp_c: float

    @classmethod
    def from_data(cls, data: dict) -> "Forecast":
        dt = datetime.strptime(data["time"], "%Y-%m-%d %H:%M")
        return cls(dt=dt, temp_c=data["temp_c"], precip_mm=data["precip_mm"])

    @classmethod
    def get_today(cls) -> list["Forecast"]:
        with httpx.Client() as c:
            res = c.get(const.WEATHER_FORECAST_URL).json()
        return [cls.from_data(x) for x in res["forecast"]["forecastday"][0]["hour"]]

    def get_hour_forecast(self, hour: int) -> Optional["Forecast"]:
        if hour == self.dt.hour:
            return self
        else:
            return None

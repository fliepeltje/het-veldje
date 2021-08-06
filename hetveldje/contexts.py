from dataclasses import dataclass
from hetveldje.types import Gender, DayName
from hetveldje.services.baserow import Dog
from hetveldje.services.weather import Forecast
from hetveldje.utils import get_day_name, get_dog_age
from datetime import date, datetime


@dataclass
class DogCtx:
    index: int
    picture_url: str
    gender: Gender
    name: str
    owner_name: str
    type: str
    extra: list[str]
    field_times: list[tuple[DayName, str]]  # (dayname, joined times)
    age: tuple[str, str]  # (years, months)

    @classmethod
    def construct(cls, index: int, dog: Dog) -> "DogCtx":
        age_delta = get_dog_age(dog.dob)
        return cls(
            index=index,
            picture_url=dog.picture,
            gender=dog.gender,
            name=dog.dog_name,
            owner_name=dog.owner_name,
            extra=dog.extra,
            type=dog.dog_type,
            field_times=[(get_day_name(d), " | ".join(t)) for d, t in dog.times],
            age=(str(age_delta.years), str(age_delta.months)),
        )


@dataclass
class DogListCtx:
    """Renders to dog-list.html"""

    dogs: list[DogCtx]

    @classmethod
    def construct(cls, dogs: list[Dog]) -> "DogListCtx":
        return cls(dogs=[DogCtx.construct(i, d) for i, d in enumerate(dogs)])


@dataclass
class HourStatCtx:
    hour_str: str
    present_dogs: list[tuple[str, str]]  #  (dogname, ownername)
    precip_mm: float
    temp_c: float

    @classmethod
    def construct(
        cls, hour: int, dogs: list[Dog], forecasts: list[Forecast]
    ) -> "HourStatCtx":
        today = date.today()
        day_num = today.weekday()
        filtered_dogs = [d for d in dogs if d.get_ranged_time(day_num, hour)]
        present = [(d.dog_name, d.owner_name) for d in filtered_dogs]
        forecast = [x for x in forecasts if x.get_hour_forecast(hour)][0]
        hour_str = f"0{hour}:00" if hour < 10 else f"{hour}:00"
        return cls(
            hour_str=hour_str,
            present_dogs=present,
            precip_mm=forecast.precip_mm,
            temp_c=forecast.temp_c,
        )


@dataclass
class LandingCtx:
    """Renders to landing.html"""

    hour_stats: list[HourStatCtx]

    @classmethod
    def construct(cls, dogs: list[Dog], forecasts: list[Forecast]) -> "LandingCtx":
        now = datetime.now().hour
        _range = range(now, now + 5)
        hour_range = [x for x in _range if x < 24]
        return cls(
            hour_stats=[HourStatCtx.construct(h, dogs, forecasts) for h in hour_range]
        )

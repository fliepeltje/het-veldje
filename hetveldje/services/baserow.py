import httpx
from dataclasses import dataclass
from datetime import date, datetime
from hetveldje import constants as const
from hetveldje.types import DayNumber, Gender
from hetveldje.utils import hour_string_to_today_dt
from typing import Optional


@dataclass
class Dog:
    dog_name: str
    dog_type: str
    owner_name: str
    picture: str
    gender: Gender
    extra: list[str]
    dob: date
    times: list[tuple[DayNumber, list[str]]]

    @staticmethod
    def parse_times_data(data: dict) -> list[tuple[DayNumber, list[str]]]:
        def key_to_day(key: str) -> DayNumber:
            _, _, num_str = key.partition("_")
            num = int(num_str)
            table: list[DayNumber] = [0, 1, 2, 3, 4, 5, 6]
            try:
                return table[num]
            except IndexError:
                raise ValueError

        return [
            (key_to_day(key), [x.strip() for x in value.split(",")])
            for key, value in data.items()
        ]

    def get_ranged_time(self, day_num: int, hour: int) -> Optional[datetime]:
        times = [t for d, t in self.times if d == day_num]
        if not times:
            return None
        time_list = [hour_string_to_today_dt(x) for x in times[0]]
        in_range = [x for x in time_list if x.hour >= hour and x.hour < hour + 1]
        if not in_range:
            return None
        else:
            return in_range[0]

    @classmethod
    def from_data(cls, data: dict) -> "Dog":
        times_data = {k: v for k, v in data.items() if k.startswith("times_")}
        times = cls.parse_times_data(times_data)
        gender = "F" if data["gender"]["value"] == "Vrouwtje" else "M"
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
    def get_all(cls) -> list["Dog"]:
        token = f"Token {const.BASEROW_API_KEY}"
        with httpx.Client(headers={"Authorization": token}) as c:
            res = c.get(const.BASEROW_DOG_TABLE_URL).json()
        return [cls.from_data(r) for r in res["results"]]

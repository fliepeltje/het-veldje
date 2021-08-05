import toml
import os
from pydantic import BaseModel
from typing import Literal


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


class Dog(BaseModel):
    dog_name: str
    dog_type: str
    owner_name: str
    picture: str
    extra: list[str]
    times: list[FieldDay]

    @classmethod
    def from_toml_path(cls, filename: str) -> "Dog":
        with open(f"content/dogs/{filename}", "r") as f:
            data = toml.load(f)
        days_data = data.pop("days")
        times = [FieldDay(**x) for x in days_data]
        return cls(times=times, **data)

    @classmethod
    def from_content(cls) -> list["Dog"]:
        return [cls.from_toml_path(p) for p in os.listdir("content/dogs")]

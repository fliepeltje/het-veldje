import os
from datetime import date
from typing import Literal

import httpx
from pydantic import BaseModel


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

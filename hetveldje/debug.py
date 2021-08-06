from hetveldje.services.baserow import Dog
from hetveldje.services.weather import Forecast
from datetime import date, datetime
import random


def generate_times():
    hours = list(range(0, 24))
    minutes = list(range(0, 59))
    res = []
    for d in range(0, 7):
        times = [0, 1, 2, 4]
        current_times = []
        for _ in range(0, random.choice(times)):
            ctime = f"{random.choice(hours)}:{random.choice(minutes)}"
            if ctime not in current_times:
                current_times.append(ctime)
        res.append((d, current_times))
    return res


def generate_dog(num) -> Dog:
    names = ["Maika", "Sneeuwbal", "Snuffel", "Pluisje"]
    owners = ["Donatas", "Henk", "Piet", "Grietje"]
    pics = [
        "https://random.dog/e9e42395-e3ec-4c1b-81ab-3506693e2efc.JPG",
        "https://random.dog/d7ae7fc7-e254-45da-8ac4-6afb898b6cc2.png",
        "https://random.dog/510a4438-2cf4-49ea-8f0f-ef0ad11999e5.jpg",
    ]
    return Dog(
        dog_name=f"{random.choice(names)}-{num}",
        owner_name=f"{random.choice(owners)}-{num}",
        dog_type="Droeftoeter",
        picture=random.choice(pics),
        gender="F" if num % 2 == 0 else "M",
        extra=["allergisch voor gluten"],
        dob=date.today(),
        times=generate_times(),  # type: ignore
    )


def generate_dogs() -> list[Dog]:
    return [generate_dog(i) for i in range(0, 15)]


def generate_forecast() -> list[Forecast]:
    today = date.today()
    res = []
    for i in range(0, 24):
        res.append(
            Forecast(
                dt=datetime(today.year, today.month, today.day, i, 0),
                precip_mm=random.choice([0.0, 0.4, 3.7]),
                temp_c=random.choice([12.3, 20.4, 34.5]),
            )
        )
    return res

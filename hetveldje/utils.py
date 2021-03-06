from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from pytz import timezone

from hetveldje.types import DayName, DayNumber


def current_dt() -> datetime:
    amsterdam = timezone("Europe/Amsterdam")
    return datetime.now(amsterdam)


def get_day_name(day_nr: DayNumber) -> DayName:
    lookup: dict[DayNumber, DayName] = {
        0: "Maandag",
        1: "Dinsdag",
        2: "Woensdag",
        3: "Donderdag",
        4: "Vrijdag",
        5: "Zaterdag",
        6: "Zondag",
    }
    return lookup[day_nr]


def get_dog_age(dob: date) -> relativedelta:
    end = datetime.fromordinal(date.today().toordinal())
    start = datetime.fromordinal(dob.toordinal())
    return relativedelta(end, start)


def hour_string_to_today_dt(hour_str: str) -> datetime:
    if ":" in hour_str:
        h, _, m = hour_str.partition(":")
    elif "." in hour_str:
        h, _, m = hour_str.partition(".")
    else:
        raise ValueError("Invalid time separator")
    today = date.today()
    return datetime(today.year, today.month, today.day, int(h), int(m))

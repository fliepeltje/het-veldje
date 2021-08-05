from datetime import datetime
from pytz import timezone


def current_dt() -> datetime:
    amsterdam = timezone("Europe/Amsterdam")
    return datetime.now(amsterdam)

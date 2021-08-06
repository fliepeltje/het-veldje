import os

# Keys
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
BASEROW_API_KEY = os.environ["BASEROW_API_KEY"]

# Urls
BASEROW_FORM_URL = os.environ["BASEROW_FORM_URL"]
BASEROW_DOG_TABLE_URL = (
    "https://api.baserow.io/api/database/rows/table/26193/?user_field_names=true"
)
WEATHER_FORECAST_BASE = "http://api.weatherapi.com/v1/forecast.json"
WEATHER_FORECAST_Q = "q=52.073938,5.086407&days=1&aqi=no&alerts=no"
WEATHER_FORECAST_URL = (
    f"{WEATHER_FORECAST_BASE}?key={WEATHER_API_KEY}&{WEATHER_FORECAST_Q}"
)

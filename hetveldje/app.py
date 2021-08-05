from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from hetveldje.types import Dog, HourForecast, HourData

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/dogs", response_class=HTMLResponse)
async def dog_list(request: Request):
    return templates.TemplateResponse(
        "dog-list.html", {"request": request, "dogs": Dog.from_api()}
    )


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    forecasts = HourForecast.from_api()
    dogs = Dog.from_api()
    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "next_five": HourData.next_5(forecasts=forecasts, dogs=dogs),
        },
    )

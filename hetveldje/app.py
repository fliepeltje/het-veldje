from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from hetveldje.services.baserow import Dog
from hetveldje.services.weather import Forecast
from hetveldje.contexts import LandingCtx, DogListCtx

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/dogs", response_class=HTMLResponse)
async def dog_list(request: Request):
    dogs = Dog.get_all()
    return templates.TemplateResponse(
        "dog-list.html", {"request": request, "ctx": DogListCtx.construct(dogs)}
    )


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    forecasts = Forecast.get_today()
    dogs = Dog.get_all()
    return templates.TemplateResponse(
        "landing.html",
        {
            "request": request,
            "ctx": LandingCtx.construct(forecasts=forecasts, dogs=dogs),
        },
    )

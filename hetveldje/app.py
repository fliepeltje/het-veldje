from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from hetveldje.types import Dog

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/dogs", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        "dog-list.html", {"request": request, "dogs": Dog.from_content()}
    )

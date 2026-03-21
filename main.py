from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.api import router

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

app.include_router(router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
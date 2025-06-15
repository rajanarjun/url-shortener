from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import AnyHttpUrl, BaseModel, ValidationError, \
        field_validator
from datetime import datetime
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class URLModel(BaseModel):
    url: AnyHttpUrl

    @field_validator("url")
    @classmethod
    def custom_validator(cls, v):
        if "." not in v.host:
            raise ValueError("Invalid URL.")
        if v.host.startswith((".","-","_","/")):
            raise ValueError("Invalid URL.")
        if v.host == "localhost":
            raise ValueError("Invalid URL.")
        return v


def validate_url(url: str):
    try:
        valid_url = URLModel(url=url)
        return valid_url.url
    except ValidationError as e:
        raise ValueError("Invalid URL.")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",{
        "request": request,
        "input_value": None,
        "error": None})


@app.post("/shorturl")
def short_url(request: Request, long_url: str = Form(...)):
    try:
        valid_url = validate_url(long_url)
    except ValueError:
        return templates.TemplateResponse("index.html",{
            "request": request,
            "input_value": long_url,
            "error": "Invalid URL. Please enter a valid URL."
            })
        
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    short_url = "https://short.ly/abc123"
    return templates.TemplateResponse("result.html",{
        "request": request,
        "original": valid_url,
        "short": short_url
        })


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

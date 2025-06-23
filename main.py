from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import AnyHttpUrl, BaseModel, ValidationError, \
        field_validator
import uvicorn
import db

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
        
    db_id = db.insert_db(long_url)
    print(db_id)

    # base62 encoding

    short_url = " "
    return templates.TemplateResponse("result.html",{
        "request": request,
        "original": valid_url,
        "short": short_url
        })


@app.get("/{short_id}")
def redirect_to_long(short_id: str):
    long_url = ""
    # TODO: implement this db lookup
    # long_url = db_lookup(short_id)
    if long_url:
        return RedirectResponse(long_url)
    else:
        raise HTTPException(status_code=404)

if __name__ == "__main__":
    db.initialize_db()
    uvicorn.run(app, host="127.0.0.1", port=8000)
    db.close_db()

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import AnyHttpUrl, BaseModel, ValidationError, \
    field_validator
import uvicorn
import db
import base62
from config import settings


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
  db.initialize_db(
     db_name=settings.DB_NAME,
     db_host=settings.DB_HOST,
     db_user=settings.DB_USER,
     db_pasw=settings.DB_PASW,
     db_port=settings.DB_PORT
  )


@app.on_event("shutdown")
def shutdown():
  db.close_db()


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
  # base62 encoding
  encoded_string = base62.encode(db_id)
  short_url = f"{settings.BASE_URL}/su/{encoded_string}"

  return templates.TemplateResponse("result.html",{
    "request": request,
    "original": valid_url,
    "short": short_url
    })


@app.get("/su/{short_id}")
def redirect_to_long(short_id: str):

  # base62 decoding
  serial_id = base62.decode(short_id)
  long_url = db.redirect_lookup(serial_id)

  if long_url:
    return RedirectResponse(long_url)
  else:
    raise HTTPException(status_code=404)


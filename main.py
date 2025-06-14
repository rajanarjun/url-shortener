from fastapi import FastAPI, Form

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg" : "URL Shortener. Use /shorturl to POST long URLs."}


@app.post("/shorturl")
def short_url(long_url: str = Form(...)):
    return {"recv url" : long_url} 

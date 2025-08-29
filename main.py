from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

import yf_fetch

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "static" / "index.html"


@app.get("/api/v1/tickers/{ticker}/expiries")
def get_expiries(ticker: str):
    return {"data": yf_fetch.fetch_option_expiries(ticker)}


@app.get("/api/v1/tickers/{ticker}/expiries/{expiry}")
def get_expiry(ticker: str, expiry: str):
    return {"data": yf_fetch.fetch_option_chain(ticker, expiry)}


app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(_: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return FileResponse(INDEX_FILE, status_code=200)
    raise exc

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

import yf_fetch

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "static" / "index.html"


class GetExpiriesResponse(BaseModel):
    expiries: list[str]


@app.get(
    "/api/v1/tickers/{ticker}/expiries",
    response_model=GetExpiriesResponse,
    operation_id="get_expiries",
)
def get_expiries(ticker: str):
    expiries = yf_fetch.fetch_option_expiries(ticker)
    return GetExpiriesResponse(expiries=expiries)


class OptionData(BaseModel):
    underlying: str
    contract: str
    expiry: str
    strike: float
    kind: str
    bid: float
    ask: float
    oi: int
    iv: float
    timestamp: datetime


class GetExpiryResponse(BaseModel):
    options: list[OptionData]


@app.get(
    "/api/v1/tickers/{ticker}/expiries/{expiry}",
    response_model=GetExpiryResponse,
    operation_id="get_expiry",
)
def get_expiry(ticker: str, expiry: str):
    options = yf_fetch.fetch_option_chain(ticker, expiry)
    return GetExpiryResponse(options=options)


app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(_: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return FileResponse(INDEX_FILE, status_code=200)
    raise exc

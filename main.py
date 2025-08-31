from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

import yf_fetch

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "static" / "index.html"


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


class GetOptionsResponse(BaseModel):
    expiries: list[str]
    options: list[OptionData]


@app.get(
    "/api/v1/tickers/{ticker}/options",
    response_model=GetOptionsResponse,
    operation_id="get_options",
)
def get_options(ticker: str, expiry: Optional[str] = Query(default=None)):
    expiries = yf_fetch.fetch_option_expiries(ticker)

    if expiry is None:
        expiry = expiries[0]

    options = yf_fetch.fetch_option_chain(ticker, expiry)

    return GetOptionsResponse(expiries=expiries, options=options)


app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(_: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return FileResponse(INDEX_FILE, status_code=200)
    raise exc

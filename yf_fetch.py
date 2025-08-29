from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf

from logger import logger


def fetch_option_expiries(ticker: str) -> list[str]:
    return yf.Ticker(ticker).options


def fetch_option_chain(ticker: str, expiry: str) -> list[dict]:
    logger.debug(f"fetching underlying={ticker} expiry={expiry}")

    ticker_data = yf.Ticker(ticker)
    now = datetime.now()
    option_chain = ticker_data.option_chain(expiry)

    clean_option_df(option_chain.calls, ticker, expiry, now)
    option_chain.calls["kind"] = "call"
    calls = option_chain.calls.to_dict(orient="records")

    clean_option_df(option_chain.puts, ticker, expiry, now)
    option_chain.puts["kind"] = "put"
    puts = option_chain.puts.to_dict(orient="records")

    options = calls + puts
    return options


def clean_option_df(df: pd.DataFrame, ticker: str, expiry: str, now: datetime):
    df["expiry"] = expiry
    df["underlying"] = ticker
    df["timestamp"] = now
    df.rename(
        columns={
            "contractSymbol": "contract",
            "openInterest": "oi",
            "impliedVolatility": "iv",
        },
        inplace=True,
    )
    df.replace(np.nan, None, inplace=True)

import os
import random
from datetime import datetime
from time import sleep

import numpy as np
import psycopg
import yfinance as yf
from dotenv import load_dotenv
from pypika import Query, Table

load_dotenv()

yf_quotes_table = Table("yf_quotes")

yf_quotes_latest_table = Table("yf_quotes_latest")

yf_options_columns = [
    "underlying",
    "contract",
    "expiry",
    "strike",
    "kind",
    "bid",
    "ask",
    "oi",
    "iv",
    "timestamp",
]


def fetch_option_expiries(conn, ticker: str):
    query = (
        Query.from_(yf_quotes_table)
        .select(yf_quotes_table.expiry)
        .distinct()
        .where(yf_quotes_table.underlying == ticker)
        .orderby(yf_quotes_table.expiry)
    )
    cur: psycopg.Cursor = conn.cursor()
    cur.execute(str(query))
    return [item["expiry"] for item in cur.fetchall()]


def fetch_option_expiry(conn, ticker: str, expiry: str):
    query = (
        Query.from_(yf_quotes_latest_table)
        .select("*")
        .where(
            (yf_quotes_latest_table.underlying == ticker)
            & (yf_quotes_latest_table.expiry == expiry)
        )
    )
    cur: psycopg.Cursor = conn.cursor()
    cur.execute(str(query))
    return cur.fetchall()


def fetch_option_chain_from_yf(ticker: str, expiry: str):
    print(f"[{datetime.now()}] fetching underlying={ticker} expiry={expiry}")

    ticker_data = yf.Ticker(ticker)
    now = datetime.now()
    option_chain = ticker_data.option_chain(expiry)

    df_cleanup(option_chain.calls, ticker, expiry, now)
    option_chain.calls["kind"] = "call"
    calls = option_chain.calls.to_dict(orient="records")

    df_cleanup(option_chain.puts, ticker, expiry, now)
    option_chain.puts["kind"] = "put"
    puts = option_chain.puts.to_dict(orient="records")

    options = calls + puts
    return options


def insert_option_quotes(conn, options):
    query = Query.into(yf_quotes_table).columns(tuple(yf_options_columns))
    for option in options:
        insert = []
        for column in yf_options_columns:
            insert.append(option[column])
        query = query.insert(tuple(insert))

    conn.execute(str(query))
    conn.commit()


def fetch_option_chains_from_yf(conn, ticker: str):
    for expiry in yf.Ticker(ticker).options:
        options = fetch_option_chain_from_yf(ticker, expiry)
        insert_option_quotes(conn, options)

        sleep_time = random.uniform(2, 10)
        print(f"[{datetime.now()}] sleeping for {sleep_time} seconds")
        sleep(sleep_time)


def df_cleanup(df, ticker, expiry, now):
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
    df["oi"] = df["oi"].replace(np.nan, None)
    df["bid"] = df["bid"].replace(np.nan, None)
    df["ask"] = df["ask"].replace(np.nan, None)
    df["iv"] = df["iv"].replace(np.nan, None)


if __name__ == "__main__":
    conn = psycopg.Connection.connect(os.environ["DATABASE_URL"])
    fetch_option_chains_from_yf(conn, "PLTR")
    fetch_option_chains_from_yf(conn, "AAPL")
    fetch_option_chains_from_yf(conn, "USO")
    fetch_option_chains_from_yf(conn, "MSFT")
    fetch_option_chains_from_yf(conn, "NVDA")
    conn.close()

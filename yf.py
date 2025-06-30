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

yf_options_table = Table("yf_quotes")

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


def fetch_option_chain_from_yf(conn, underlying: str):
    ticker = yf.Ticker(underlying)

    for expiry in ticker.options:
        print(f"[{datetime.now()}] fetching underlying={underlying} expiry={expiry}")

        now = datetime.now()

        def df_cleanup(df):
            df["expiry"] = expiry
            df["underlying"] = underlying
            df["timestamp"] = now
            df.rename(
                columns={
                    "contractSymbol": "contract",
                    "openInterest": "oi",
                    "impliedVolatility": "iv",
                },
                inplace=True,
            )
            df["oi"] = df["oi"].replace(np.nan, 0)

        option_chain = ticker.option_chain(expiry)

        df_cleanup(option_chain.calls)
        option_chain.calls["kind"] = "call"
        calls = option_chain.calls.to_dict(orient="records")

        df_cleanup(option_chain.puts)
        option_chain.puts["kind"] = "put"
        puts = option_chain.puts.to_dict(orient="records")

        options = calls + puts

        query = Query.into(yf_options_table).columns(tuple(yf_options_columns))
        for option in options:
            insert = []
            for column in yf_options_columns:
                insert.append(option[column])
            query = query.insert(tuple(insert))

        conn.execute(str(query))
        conn.commit()

        sleep_time = random.uniform(2, 10)
        print(f"[{datetime.now()}] sleeping for {sleep_time} seconds")

        sleep(sleep_time)


if __name__ == "__main__":
    conn = psycopg.Connection.connect(os.environ["DATABASE_URL"])
    fetch_option_chain_from_yf(conn, "PLTR")
    fetch_option_chain_from_yf(conn, "AAPL")
    fetch_option_chain_from_yf(conn, "USO")
    fetch_option_chain_from_yf(conn, "MSFT")
    fetch_option_chain_from_yf(conn, "NVDA")
    conn.close()

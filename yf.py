import os
import random
from time import sleep

import psycopg
from dotenv import load_dotenv

import yf_fetch
import yf_quotes
from logger import logger

load_dotenv()


def fetch_option_chains_from_yf(conn: psycopg.Connection, ticker: str):
    for expiry in yf_fetch.fetch_option_expiries(ticker):
        options = yf_fetch.fetch_option_chain(ticker, expiry)
        yf_quotes.insert_option_quotes(conn, options)

        logger.info(f"saved options for {ticker} {expiry}: {len(options)}")

        sleep_time = random.uniform(2, 10)
        logger.debug(f"sleeping for {sleep_time} seconds")
        sleep(sleep_time)


if __name__ == "__main__":
    conn = psycopg.Connection.connect(os.environ["DATABASE_URL"])
    fetch_option_chains_from_yf(conn, "PLTR")
    conn.close()

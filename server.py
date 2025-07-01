import json
import os

import psycopg
import yfinance as yf
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import init_chat_model
from psycopg.rows import dict_row

import yf as ylib

load_dotenv()

conn = psycopg.Connection.connect(os.environ["DATABASE_URL"], row_factory=dict_row)

model = init_chat_model("gpt-4o-mini", model_provider="openai")

app = FastAPI()

# FIXME: should be selective.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/v1/tickers/{ticker}/expiries")
def get_expiries(ticker: str):
    return {"data": ylib.fetch_option_expiries(conn, ticker)}


@app.get("/v1/tickers/{ticker}/expiries/{expiry}")
def get_expiry(ticker: str, expiry: str):
    return {"data": ylib.fetch_option_expiry(conn, ticker, expiry)}


@app.get("/v1/tickers/{ticker}/summary/")
def read_item(ticker: str):
    data = yf.Ticker(ticker=ticker)

    ai_response = model.invoke(
        f"""
            Give me a short summary on fundamental ratios based on the following data:
            {json.dumps(data.info)}
        """
    )

    ai_summary = ai_response.content

    return {"ticker": data.info, "aiSummary": ai_summary}

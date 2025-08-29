import psycopg
from pypika import Query, Table

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


def query_option_expiry(conn: psycopg.Connection, ticker: str, expiry: str):
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


def query_option_expiries(conn: psycopg.Connection, ticker: str) -> list[str]:
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


def insert_option_quotes(conn: psycopg.Connection, options: list[dict]):
    query = Query.into(yf_quotes_table).columns(tuple(yf_options_columns))
    for option in options:
        insert = []
        for column in yf_options_columns:
            insert.append(option[column])
        query = query.insert(tuple(insert))
    conn.execute(str(query))
    conn.commit()

CREATE TABLE yf_quotes
(
    underlying      TEXT,
    contract        TEXT,
    expiry          DATE,
    strike          DECIMAL,
    kind            TEXT,
    bid             DECIMAL,
    ask             DECIMAL,
    oi              INT,
    iv              DECIMAL,
    timestamp       TIMESTAMP,
    PRIMARY KEY (contract)
)

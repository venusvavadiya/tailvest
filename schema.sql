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
    PRIMARY KEY (contract, timestamp)
)

CREATE VIEW yf_quotes_latest AS
SELECT DISTINCT ON (contract) *
FROM yf_quotes
ORDER BY contract, timestamp DESC;

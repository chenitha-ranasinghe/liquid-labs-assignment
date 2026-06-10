import sqlite3

DB_NAME = "market_data.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS monthly_data(
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT    NOT NULL,
        date   TEXT    NOT NULL,
        high   REAL    NOT NULL,
        low    REAL    NOT NULL,
        volume INTEGER NOT NULL,
        UNIQUE(symbol, date)
    )
    """)
    conn.commit()
    conn.close()

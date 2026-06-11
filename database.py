import sqlite3

DB_NAME = "market_data.db"

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()
    try:
        connection.execute("""
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
        connection.commit()
    finally:
        connection.close()

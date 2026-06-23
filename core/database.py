import sqlite3

class DatabaseManager:
    def __init__(self, db_name = "market_db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        #Establish a connection and a cursor
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        schema_query ="""
        CREATE TABLE IF NOT EXISTS crypto_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin TEXT,
        price REAL,
        timestamp TEXT,
        log_price REAL,
        normalized_price REAL
        )
        """

        cursor.execute(schema_query)
        conn.commit()
        conn.close()
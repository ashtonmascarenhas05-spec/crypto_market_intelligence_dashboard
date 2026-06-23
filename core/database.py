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
    
    def insert_row(self, row):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Notice the question marks! These are secure placeholders.
        insert_query = """
        INSERT INTO crypto_data (coin, price, timestamp, log_price, normalized_price)
        VALUES (?, ?, ?, ?, ?)
        """

        # We pass the exact values from your Pandas tuple to fill in the question marks
        # (row.coin, row.price, str(row.timestamp), row.log_price, row.normalized_price)
        
        # --- YOUR TURN TO FINISH THIS ---
        # How do you execute the query, commit the changes, and close the connection?
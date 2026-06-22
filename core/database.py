import sqlite3

class DatabaseManager:
    def __init__(self, db_name = "market_db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        #Queries to create a  table has to be written here
        pass
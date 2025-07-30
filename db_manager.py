import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_name='currency_converter.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            from_currency TEXT,
            to_currency TEXT,
            converted_amount REAL,
            timestamp TEXT
        )
        ''')
        self.conn.commit()

    def save_conversion(self, amount, from_curr, to_curr, converted_amt):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO conversions (amount, from_currency, to_currency, converted_amount, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (amount, from_curr, to_curr, converted_amt, timestamp))
        self.conn.commit()

    def fetch_all_conversions(self):
        self.cursor.execute("SELECT * FROM conversions ORDER BY id DESC")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

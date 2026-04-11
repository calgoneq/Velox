import sqlite3

class PriceRepository:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS prices (id INTEGER PRIMARY KEY, crypto_id TEXT, open_price REAL, high REAL, low REAL, close REAL, timestamp TEXT)')

    def save(self, crypto_id: str, open_price: float, high: float, low: float, close: float, timestamp: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO prices (crypto_id, open_price, high, low, close, timestamp) VALUES (?, ?, ?, ?, ?, ?)", (crypto_id, open_price, high, low, close, timestamp))

    def get_last_n_prices(self, n: int) -> list[float]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT open_price, high, low, close FROM prices ORDER BY id DESC LIMIT ?", (n,))
            data = cursor.fetchall()
            
            return [row for row in data]
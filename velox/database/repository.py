import sqlite3

class PriceRepository:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS prices (id INTEGER PRIMARY KEY, crypto_id TEXT, price REAL, timestamp TEXT)')

    def save(self, crypto_id: str, price: float, timestamp: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO prices (crypto_id, price, timestamp) VALUES (?, ?, ?)", (crypto_id, price, timestamp))

    def get_last_n_prices(self, n: int) -> list[float]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()  # Tu tworzymy "długopis" do bazy
            cursor.execute("SELECT price FROM prices ORDER BY id DESC LIMIT ?", (n,))
            data = cursor.fetchall() # Tu wyciągamy dane "długopisem"
            return [row[0] for row in data]
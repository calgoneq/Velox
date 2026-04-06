import requests
import time
from datetime import datetime
import sqlite3

TARGET_CRYPTO = "bitcoin"

def init_db() -> None:
    conn = sqlite3.connect('crypto.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS prices (id INTEGER PRIMARY KEY, crypto_id TEXT, price REAL, timestamp TEXT)')
    conn.commit()
    conn.close()

def save_to_db(conn, crypto_id: str, price: float, timestamp: str) -> None:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prices (crypto_id, price, timestamp) VALUES (?, ?, ?)", (crypto_id, price, timestamp))
    conn.commit()

def get_price(crypto_id: str) -> float:
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd'
    r = requests.get(url)
    r.raise_for_status()

    data = r.json()
    price = data[crypto_id]["usd"]
    return price

if __name__ == "__main__":
    init_db()
    conn = sqlite3.connect('crypto.db')
    price_counter = 0

    while price_counter < 5:       
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            price = get_price(crypto_id=TARGET_CRYPTO)
            save_to_db(conn=conn, crypto_id=TARGET_CRYPTO, price=price, timestamp=timestamp)
            print(f"Record added {price_counter}")

            price_counter += 1

            if price_counter < 5:
                time.sleep(10)

        except requests.exceptions.RequestException as e:
            print(f"Błąd sieci/API w próbie {price_counter+1}: {e}")
            time.sleep(60)
        except KeyError as e:
            print(f"Błąd: Nie znaleziono klucza w odpowiedzi API. Treść odpowiedzi: {e}")
    
    conn.close()
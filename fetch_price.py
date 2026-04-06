import requests
import time
from datetime import datetime
import sqlite3
from dotenv import load_dotenv
import os
from groq import Groq
import sys

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

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

def get_latest_prices(conn) -> list[float]:
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM prices ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    prices: list[float] = [row[0] for row in rows]

    return prices

def analyze_price(prices: list[float], api_key: str) -> str:
    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f'''
                    I have these 5 Bitcoin prices from the last 2 minutes: {prices}.
                    Act as a crypto analyst. Is the trend going up or down? Answer in 1 sentence.
                ''',
            }
        ],
        model="openai/gpt-oss-20b",
    )
    print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    if not groq_api_key:
        print("BŁĄD: Brak zmiennej środowiskowej GROQ_API_KEY")
        sys.exit(1)

    init_db()
    conn = sqlite3.connect('crypto.db')
    price_counter = 0

    while price_counter < 5:       
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            price = get_price(crypto_id=TARGET_CRYPTO)
            save_to_db(conn=conn, crypto_id=TARGET_CRYPTO, price=price, timestamp=timestamp)

            price_counter += 1
            print(f"Record {price_counter} added")

            if price_counter < 5:
                time.sleep(10)

        except requests.exceptions.RequestException as e:
            print(f"Błąd sieci/API w próbie {price_counter+1}: {e}")
            time.sleep(60)
        except KeyError as e:
            print(f"Błąd: Nie znaleziono klucza w odpowiedzi API. Treść odpowiedzi: {e}")
    
    prices = get_latest_prices(conn=conn)
    analyze_price(prices=prices, api_key=groq_api_key)
    conn.close()
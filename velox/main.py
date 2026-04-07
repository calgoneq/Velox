from datetime import datetime
import sqlite3
import requests
import time
from dotenv import load_dotenv
import sys
import os

from velox.fetcher.coingecko import get_price
from velox.database.repository import PriceRepository
from velox.analysis.analyzer import analyze_price
from velox.config import CRYPTO_ID, DB_NAME, AMOUNT_TO_FETCH, RETRIES, API_URL
from velox.analysis.indicators.rsi import calculate_rsi

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")
repo = PriceRepository(DB_NAME)

if __name__ == "__main__":
    if not groq_api_key:
        print("ERROR: GROQ_API_KEY environment variable is not set.")
        sys.exit(1)

    repo.init_db()
    price_counter = 0

    while price_counter < RETRIES:       
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            price = get_price(crypto_id=CRYPTO_ID, api_url=API_URL)
            repo.save(crypto_id=CRYPTO_ID, price=price, timestamp=timestamp)

            price_counter += 1
            print(f"Record {price_counter} added")

            if price_counter < RETRIES:
                time.sleep(10)

        except requests.exceptions.RequestException as e:
            print(f"Network/API error on attempt {price_counter + 1}: {e}")
            time.sleep(60)
        except KeyError as e:
            print(f"Error: Key not found in API response. Response content: {e}")

    prices = repo.get_last_n_prices(n=AMOUNT_TO_FETCH)
    rsi = calculate_rsi(prices=prices)
    analyze_price(prices=prices, api_key=groq_api_key, rsi=rsi)
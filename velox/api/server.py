from fastapi import FastAPI
from datetime import datetime
import os

from velox.database.repository import PriceRepository
from velox.analysis.utils import unpack_prices
from velox.analysis.indicators.rsi import calculate_rsi
from velox.analysis.indicators.fvg import detect_fvg
from velox.analysis.indicators.msa import detect_swings, calculate_sentiment_msa
from velox.analysis.analyzer import analyze_price
from velox.fetcher.binance import get_price
from velox.config import AMOUNT_TO_FETCH, PERIOD, PERCENT, DB_NAME, CRYPTO_ID, API_URL

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Velox Crypto Bot API is running"}

@app.get("/analyze")
def get_analysis():
    repo = PriceRepository(DB_NAME)
    repo.init_db()
    prices = repo.get_last_n_prices(n=AMOUNT_TO_FETCH)
    open_prices, highs, lows, closes = unpack_prices(prices)
    rsi_v = calculate_rsi(closes=closes, period=PERIOD)
    fvg_v = len(detect_fvg(highs=highs, lows=lows, closes=closes, percent=PERCENT))
    msa = detect_swings(highs=highs, lows=lows, closes=closes)
    msa_v = calculate_sentiment_msa(msa=msa, closes=closes)

    api_key = os.getenv("GROQ_API_KEY")
    ai_response = analyze_price(closes, api_key, rsi_v, fvg_v, msa_v)
    
    return {"ai_decision": ai_response}

@app.get("/fetch")
async def fetch_data():
    price_data = await get_price(CRYPTO_ID, API_URL)
    
    repo = PriceRepository(DB_NAME)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    repo.save(CRYPTO_ID, price_data[0], price_data[1], price_data[2], price_data[3], timestamp)
    
    return {"status": "success", "new_price": price_data[3]}
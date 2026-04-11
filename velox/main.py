from datetime import datetime
import httpx
from dotenv import load_dotenv
import sys
import os
import logging
import asyncio

from velox.fetcher.binance import get_price
from velox.database.repository import PriceRepository
from velox.analysis.analyzer import analyze_price
from velox.config import CRYPTO_ID, DB_NAME, AMOUNT_TO_FETCH, SAMPLES_TO_COLLECT, API_URL, PERCENT, PERIOD
from velox.analysis.indicators.rsi import calculate_rsi
from velox.analysis.indicators.fvg import detect_fvg, calculate_sentiment_fvg
from velox.analysis.indicators.msa import detect_swings, calculate_sentiment_msa
from velox.analysis.utils import unpack_prices

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")
repo = PriceRepository(DB_NAME)

async def main():
    if not groq_api_key:
        logger.error("ERROR: GROQ_API_KEY environment variable is not set.")
        sys.exit(1)

    repo.init_db()
    price_counter = 0

    while price_counter < SAMPLES_TO_COLLECT:       
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            price = await get_price(crypto_id=CRYPTO_ID, api_url=API_URL)
            print(price)

            repo.save(crypto_id=CRYPTO_ID, open_price=price[0], high=price[1], low=price[2], close=price[3], timestamp=timestamp)

            price_counter += 1
            logger.info(f"Record {price_counter} added successfully")

            if price_counter < SAMPLES_TO_COLLECT:
                await asyncio.sleep(3)

        except httpx.HTTPError as e:
            logger.error(f"Network/API error on attempt {price_counter + 1}: {e}")
            await asyncio.sleep(60)
        except KeyError as e:
            logger.error(f"Key not found in API response. Response content: {e}")

    prices = repo.get_last_n_prices(n=AMOUNT_TO_FETCH)
    open_prices, highs, lows, closes = unpack_prices(prices)

    rsi = calculate_rsi(closes=closes, period=PERIOD)
    fvg = detect_fvg(highs=highs, lows=lows, closes=closes, percent=PERCENT)
    fvg_sentiment_score = calculate_sentiment_fvg(fvg=fvg)
    msa = detect_swings(highs=highs, lows=lows, closes=closes)
    msa_sentiment_score = calculate_sentiment_msa(msa=msa, closes=closes)

    result = analyze_price(closes=closes, api_key=groq_api_key, rsi=rsi, fvg=fvg_sentiment_score, msa=msa_sentiment_score)
    logger.info(result)

if __name__ == "__main__":
    asyncio.run(main())
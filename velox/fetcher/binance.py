from velox.config import API_URL, CRYPTO_ID
import httpx

async def get_price(crypto_id: str, api_url: str) -> list:
    url = f'{api_url}?symbol={crypto_id}&interval=1m&limit=1'
    
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()

        data = r.json()
        open_price = data[0][1]
        high = data[0][2]
        low = data[0][3]
        close = data[0][4]

        candle_data = [open_price, high, low, close]

        return candle_data
import httpx

async def get_price(crypto_id: str, api_url: str) -> float:
    url = f'{api_url}?ids={crypto_id}&vs_currencies=usd'
    
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()

        data = r.json()
        return data[crypto_id]["usd"]
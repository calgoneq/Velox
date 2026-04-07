import requests

def get_price(crypto_id: str, api_url: str) -> float:
    url = f'{api_url}?ids={crypto_id}&vs_currencies=usd'
    r = requests.get(url)
    r.raise_for_status()

    data = r.json()
    price = data[crypto_id]["usd"]
    return price
import requests

url = f'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
r = requests.get(url)
r.raise_for_status()

data = r.json()
price = data["bitcoin"]["usd"]

print(f"Current price: {price} USD")
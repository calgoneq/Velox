import requests
import time

TARGET_CRYPTO = "bitcoin"

def get_price(crypto_id: str) -> float:
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd'
    r = requests.get(url)
    r.raise_for_status()

    data = r.json()
    price = data[crypto_id]["usd"]
    return price

if __name__ == "__main__":
    price_counter = 0

    while price_counter < 5:       
        try:
            price = get_price(crypto_id=TARGET_CRYPTO)
            print(f"Current price: {price} USD")

            price_counter += 1

            if price_counter < 5:
                time.sleep(10)

        except requests.exceptions.RequestException as e:
            print(f"Błąd sieci/API w próbie {price_counter+1}: {e}")
            time.sleep(60)
        except KeyError as e:
            print(f"Błąd: Nie znaleziono klucza w odpowiedzi API. Treść odpowiedzi: {e}")
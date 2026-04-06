# Velox

# Co to jest?
Prosta aplikacja terminalowa służąca do pobrania ostatnich N cen kryptowaluty oraz zdecydowaniu przy pomocy api calli do modelu openai/gpt-oss-20b czy jest to trend rosnący czy malejący.

# Jak uruchomić?
docker pull calgoneq/velox:latest
docker run --rm -e GROQ_API_KEY=twoj_klucz calgoneq/velox:latest

Lub jeśli masz klucz w pliku `.env` w katalogu projektu:
docker run --rm --env-file .env calgoneq/velox:latest

# Zmienne środowiskowe:
GROQ_API_KEY = klucz api z strony: https://console.groq.com/keys
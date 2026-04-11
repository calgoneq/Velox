def detect_swings(highs: list[float], lows: list[float], closes: list[float]) -> dict:
    max_high = max(highs)
    min_low = min(lows)

    swings = {"high": max_high, "low": min_low}

    return swings

def calculate_sentiment_msa(msa: dict, closes: list[float]) -> int:
    last_close = closes[-1]

    if last_close > msa['high']:
        return 1
    elif last_close < msa['low']:
        return -1
    else:
        return 0
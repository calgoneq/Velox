def detect_swings(prices: list[tuple]) -> dict:

    highs = [candle[1] for candle in prices[:-1]]
    lows = [candle[2] for candle in prices[:-1]]

    max_high = max(highs)
    min_low = min(lows)

    swings = {"high": max_high, "low": min_low}

    return swings

def calculate_sentiment_msa(msa: dict, prices: list[tuple]) -> int:
    closes = [candle[3] for candle in prices]
    last_close = closes[-1]

    if last_close > msa['high']:
        return 1
    elif last_close < msa['low']:
        return -1
    else:
        return 0
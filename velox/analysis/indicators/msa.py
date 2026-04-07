def detect_swings(prices: list[float]) -> dict:
    swings = {"highs": [], "lows": [], "neutrals": []}

    for i in range(1, len(prices) - 1):
        if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
            swings["highs"].append(prices[i])
        elif prices[i] < prices[i-1] and prices[i] < prices[i+1]:
            swings["lows"].append(prices[i])
        else:
            swings["neutrals"].append(prices[i])

    return swings

def calculate_sentiment_msa(msa: dict) -> int:
    counts = {key: len(value) for key, value in msa.items()}
    sentiment_score = (counts['highs'] * 1) + (counts['lows'] * -1) + (counts['neutrals'] * 0)
    
    return sentiment_score
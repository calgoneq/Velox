def detect_fvg(highs: list[float], lows: list[float], closes: list[float], percent: float) -> list[str]:
    fvg = []

    for i in range(2, len(closes)):
        margin = closes[i] * percent

        if lows[i] > highs[i-2] + margin:
            fvg.append("Bullish Gap")

        elif highs[i] < lows[i-2] - margin:
            fvg.append("Bearish Gap")
        
        else:
            fvg.append("None")

    return fvg

def calculate_sentiment_fvg(fvg: list[str]) -> int:
    sentiment_score = 0

    for i in fvg:
        if i == "Bullish Gap":
            sentiment_score += 1
        elif i == "Bearish Gap":
            sentiment_score -= 1
        else:
            sentiment_score += 0
    
    return sentiment_score
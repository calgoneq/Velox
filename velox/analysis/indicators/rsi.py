def calculate_rsi(prices: list[float]) -> float:

    if len(prices) < 2:
        raise ValueError("At least 2 prices are required to calculate RSI")

    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        
        if change > 0:
            gains.append(change)
        elif change < 0:
            losses.append(abs(change))

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    if avg_loss == 0:
        return 100.0
    elif avg_gain == 0:
        return 0.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
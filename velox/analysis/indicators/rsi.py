def calculate_rsi(closes: list[float], period: int) -> float:

    if len(closes) < 2:
        raise ValueError("At least 2 prices are required to calculate RSI")
    if len(closes) < period + 1:
        raise IndexError("Period can't be higher then price list")

    gains = []
    losses = []

    for i in range(1, period):
        change = closes[i] - closes[i-1]
        
        if change > 0:
            gains.append(change)
        elif change < 0:
            losses.append(abs(change))
    
    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 0

    for i in range(period, len(closes)):
        change = closes[i] - closes[i - 1]
        current_loss = 0
        current_gain = 0

        current_gain = change if change > 0 else 0
        current_loss = abs(change) if change < 0 else 0

        avg_gain = (avg_gain * (period - 1) + current_gain) / period
        avg_loss = (avg_loss * (period - 1) + current_loss) / period

    if avg_loss == 0:
        return 100.0
    elif avg_gain == 0:
        return 0.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
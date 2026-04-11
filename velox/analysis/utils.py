def unpack_prices(prices: list[tuple[float, float, float, float]]) -> list[float]:
    open_prices = [candle[0] for candle in prices]
    highs = [candle[1] for candle in prices]
    lows = [candle[2] for candle in prices]
    closes = [candle[3] for candle in prices]

    return open_prices, highs, lows, closes
import pytest
from velox.analysis.indicators.rsi import calculate_rsi
from velox.analysis.indicators.msa import detect_swings
from velox.analysis.indicators.fvg import detect_fvg

# ====================== RSI TESTS ======================

def test_calculate_rsi_only_rising():
    prices = [10, 20, 30, 40, 50]
    rsi = calculate_rsi(prices)
    assert rsi == 100.0, f"Expected 100.0, got {rsi}"

def test_calculate_rsi_only_falling():
    prices = [50, 40, 30, 20, 10]
    rsi = calculate_rsi(prices)
    assert rsi == 0.0, f"Expected 0.0, got {rsi}"

def test_calculate_rsi_short_list():
    with pytest.raises((ValueError, IndexError)):
        calculate_rsi([100])

    with pytest.raises((ValueError, IndexError)):
        calculate_rsi([])

# ====================== MSA / detect_swings TESTS ======================

def test_detect_swings_high():
    prices = [10, 20, 10]
    result = detect_swings(prices)
    
    assert len(result["highs"]) == 1
    assert 20 in result["highs"]
    assert len(result["lows"]) == 0

def test_detect_swings_low():
    prices = [20, 10, 20]
    result = detect_swings(prices)
    
    assert len(result["lows"]) == 1
    assert 10 in result["lows"]
    assert len(result["highs"]) == 0

def test_detect_swings_no_swings():
    prices = [10, 20, 30, 40, 50]
    result = detect_swings(prices)
    assert len(result["highs"]) == 0
    assert len(result["lows"]) == 0

# # ====================== FVG TESTS ======================

def test_detect_fvg_with_5_percent_gap():
    prices = [100.0, 101.0, 105.5]
    
    result = detect_fvg(prices, percent=0.01)
    
    assert "Bullish Gap" in result
    assert len(result) == 1, f"Expected 1 gap, got {len(result)}"
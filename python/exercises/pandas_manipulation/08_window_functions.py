# -*- coding: utf-8 -*-
"""
Problem: Implement window functions for financial time series analysis

Difficulty: Hard
Estimated Time: 25 minutes
Topics: rolling, expanding, ewm, window functions, financial analysis

Given stock price data:
1. Calculate rolling statistics (mean, std, min, max)
2. Compute expanding cumulative metrics
3. Use exponentially weighted moving averages (EWMA)
4. Identify when price crosses above/below the moving average

Window functions are heavily used in financial data engineering and analytics.
"""

import pandas as pd
import numpy as np


def rolling_statistics(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Calculate rolling statistics for a stock price DataFrame.

    Args:
        df: DataFrame with DatetimeIndex and columns [open, high, low, close, volume]
        window: Rolling window size in days

    Returns:
        Original DataFrame with additional columns:
        - rolling_mean: rolling mean of 'close' price
        - rolling_std: rolling standard deviation of 'close' price
        - rolling_min: rolling minimum of 'close' price
        - rolling_max: rolling maximum of 'close' price
        All rolling calculations should use min_periods=1.
        Round all new columns to 2 decimal places.
    """
    # TODO: Implement your solution here
    pass


def expanding_cumulative(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate expanding (cumulative) metrics.

    Args:
        df: DataFrame with DatetimeIndex and columns [close, volume]

    Returns:
        Original DataFrame with additional columns:
        - cumulative_max: expanding max of close price
        - cumulative_mean: expanding mean of close price, rounded to 2 decimals
        - cumulative_volume: expanding sum of volume
        - drawdown: (close - cumulative_max) / cumulative_max * 100, rounded to 2 decimals
          This shows how far the price has fallen from its all-time high.
    """
    # TODO: Implement your solution here
    pass


def ewma_signals(df: pd.DataFrame, short_span: int = 5, long_span: int = 20) -> pd.DataFrame:
    """
    Calculate exponentially weighted moving averages and generate crossover signals.

    Args:
        df: DataFrame with DatetimeIndex and a 'close' column
        short_span: Span for the short-term EWMA
        long_span: Span for the long-term EWMA

    Returns:
        Original DataFrame with additional columns:
        - ewma_short: short-term EWMA of close price, rounded to 2 decimals
        - ewma_long: long-term EWMA of close price, rounded to 2 decimals
        - signal: 'buy' when ewma_short > ewma_long, 'sell' otherwise
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def _make_stock_data() -> pd.DataFrame:
    """Create test stock data."""
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=30, freq='B')
    base_price = 100.0
    returns = np.random.normal(0.001, 0.02, size=30)
    close_prices = base_price * np.cumprod(1 + returns)

    return pd.DataFrame({
        'open': close_prices * np.random.uniform(0.98, 1.0, 30),
        'high': close_prices * np.random.uniform(1.0, 1.03, 30),
        'low': close_prices * np.random.uniform(0.97, 1.0, 30),
        'close': close_prices,
        'volume': np.random.randint(1000000, 5000000, 30)
    }, index=dates)


def test_rolling_statistics():
    """Test rolling statistics calculation."""
    df = _make_stock_data()
    result = rolling_statistics(df, window=5)

    expected_cols = ['rolling_mean', 'rolling_std', 'rolling_min', 'rolling_max']
    for col in expected_cols:
        assert col in result.columns, f"Missing column: {col}"

    # First value should equal close (min_periods=1)
    assert result['rolling_mean'].iloc[0] == round(df['close'].iloc[0], 2), \
        "First rolling_mean should equal first close with min_periods=1"

    # No NaN values
    for col in expected_cols:
        assert result[col].isnull().sum() == 0, f"{col} should have no NaN values"

    # Rolling max should always be >= rolling mean
    assert (result['rolling_max'] >= result['rolling_mean']).all(), \
        "Rolling max should be >= rolling mean"

    print("PASS: Rolling statistics work correctly")


def test_expanding_cumulative():
    """Test expanding cumulative calculations."""
    df = _make_stock_data()[['close', 'volume']]
    result = expanding_cumulative(df)

    assert 'cumulative_max' in result.columns, "Missing 'cumulative_max' column"
    assert 'drawdown' in result.columns, "Missing 'drawdown' column"

    # Cumulative max should never decrease
    assert (result['cumulative_max'].diff().dropna() >= 0).all(), \
        "Cumulative max should never decrease"

    # Drawdown should always be <= 0
    assert (result['drawdown'] <= 0.01).all(), "Drawdown should be <= 0 (with small float tolerance)"

    # Cumulative volume should always increase
    assert (result['cumulative_volume'].diff().dropna() > 0).all(), \
        "Cumulative volume should always increase"

    print("PASS: Expanding cumulative metrics work correctly")


def test_ewma_signals():
    """Test EWMA signal generation."""
    df = _make_stock_data()[['close']]
    result = ewma_signals(df, short_span=5, long_span=20)

    assert 'ewma_short' in result.columns, "Missing 'ewma_short' column"
    assert 'ewma_long' in result.columns, "Missing 'ewma_long' column"
    assert 'signal' in result.columns, "Missing 'signal' column"

    # Signals should only be 'buy' or 'sell'
    valid_signals = {'buy', 'sell'}
    actual_signals = set(result['signal'].unique())
    assert actual_signals.issubset(valid_signals), \
        f"Signals should be 'buy' or 'sell', got {actual_signals}"

    # Verify signal logic: when short > long, signal is 'buy'
    for _, row in result.iterrows():
        if row['ewma_short'] > row['ewma_long']:
            assert row['signal'] == 'buy', "Signal should be 'buy' when short EWMA > long EWMA"
        else:
            assert row['signal'] == 'sell', "Signal should be 'sell' when short EWMA <= long EWMA"

    print("PASS: EWMA signals work correctly")


if __name__ == "__main__":
    test_rolling_statistics()
    test_expanding_cumulative()
    test_ewma_signals()
    print("\nAll tests passed! Great job!")

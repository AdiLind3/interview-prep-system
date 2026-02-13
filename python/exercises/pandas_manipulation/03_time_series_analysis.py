# -*- coding: utf-8 -*-
"""
Problem: Analyze time series sales data with resampling and rolling averages

Difficulty: Medium
Estimated Time: 20 minutes
Topics: resample, rolling, time series, period comparison

Given a DataFrame of daily sales data over several months:
1. Resample daily data to weekly totals
2. Calculate a 7-day rolling average of daily sales
3. Compare month-over-month growth rates

These operations are fundamental for building dashboards and data pipelines.
"""

import pandas as pd
import numpy as np
from typing import Dict


def resample_to_weekly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resample daily sales data to weekly totals.

    Args:
        df: DataFrame with a DatetimeIndex and a 'sales' column containing daily sales.

    Returns:
        DataFrame with weekly frequency, 'sales' column summed per week.
        The index should be the start of each week (Monday).
    """
    # TODO: Implement your solution here
    pass


def rolling_average(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """
    Calculate a rolling average of daily sales.

    Args:
        df: DataFrame with a DatetimeIndex and a 'sales' column.
        window: Number of days for the rolling window.

    Returns:
        Original DataFrame with an additional 'rolling_avg' column.
        The rolling average should have min_periods=1 so early rows are not NaN.
    """
    # TODO: Implement your solution here
    pass


def month_over_month_growth(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate month-over-month growth rates.

    Args:
        df: DataFrame with a DatetimeIndex and a 'sales' column.

    Returns:
        Dictionary mapping month labels (e.g., '2024-02') to growth rate
        as a percentage relative to the previous month.
        The first month has no growth rate and should not be included.
        Round growth rates to 2 decimal places.

    Example:
        If Jan total = 1000 and Feb total = 1200:
        growth = ((1200 - 1000) / 1000) * 100 = 20.0
        Returns: {'2024-02': 20.0}
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def _make_test_data() -> pd.DataFrame:
    """Create test data: 90 days of sales data."""
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=90, freq='D')
    sales = np.random.randint(100, 500, size=90).astype(float)
    return pd.DataFrame({'sales': sales}, index=dates)


def test_resample_to_weekly():
    """Test weekly resampling."""
    df = _make_test_data()
    result = resample_to_weekly(df)

    # Should have roughly 13 weeks for 90 days
    assert len(result) >= 12, f"Expected at least 12 weeks, got {len(result)}"

    # Weekly sums should be larger than daily values
    assert result['sales'].mean() > df['sales'].mean(), "Weekly sums should exceed daily averages"

    # Index should be weekly frequency
    assert result.index.freq is not None or len(result) > 1, "Result should have a weekly index"

    print("PASS: Weekly resampling works correctly")


def test_rolling_average():
    """Test rolling average calculation."""
    df = _make_test_data()
    result = rolling_average(df, window=7)

    assert 'rolling_avg' in result.columns, "Result must have a 'rolling_avg' column"

    # First value should equal the first sales value (min_periods=1)
    assert result['rolling_avg'].iloc[0] == df['sales'].iloc[0], \
        "First rolling avg should equal first sales value with min_periods=1"

    # No NaN values
    assert result['rolling_avg'].isnull().sum() == 0, "Rolling avg should have no NaN (min_periods=1)"

    # Rolling average should be smoother (lower std) than raw data
    assert result['rolling_avg'].std() < df['sales'].std(), \
        "Rolling average should have lower variance than raw data"

    print("PASS: Rolling average works correctly")


def test_month_over_month_growth():
    """Test month-over-month growth calculation."""
    # Create controlled data
    dates = pd.date_range('2024-01-01', periods=60, freq='D')
    # January: 31 days * 100 = 3100, February: 29 days * 200 = 5800
    sales = [100.0] * 31 + [200.0] * 29
    df = pd.DataFrame({'sales': sales}, index=dates)

    result = month_over_month_growth(df)

    assert '2024-01' not in result, "First month should not have a growth rate"
    assert '2024-02' in result, "February should have a growth rate"

    # Feb total = 5800, Jan total = 3100, growth = ((5800-3100)/3100)*100 = 87.10
    expected_growth = round(((29 * 200 - 31 * 100) / (31 * 100)) * 100, 2)
    assert result['2024-02'] == expected_growth, \
        f"Expected growth {expected_growth}%, got {result['2024-02']}%"

    print("PASS: Month-over-month growth works correctly")


if __name__ == "__main__":
    test_resample_to_weekly()
    test_rolling_average()
    test_month_over_month_growth()
    print("\nAll tests passed! Great job!")

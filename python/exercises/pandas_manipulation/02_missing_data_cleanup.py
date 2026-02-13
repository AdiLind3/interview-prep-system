# -*- coding: utf-8 -*-
"""
Problem: Handle missing data in a sales DataFrame

Difficulty: Medium
Estimated Time: 15 minutes
Topics: fillna, dropna, interpolation, NaN handling

Given a DataFrame of daily sales data with missing values:
1. Fill missing 'category' values with 'Unknown'
2. Fill missing 'price' values with the median price per category
3. Drop rows where more than half the columns are NaN
4. Interpolate missing 'units_sold' values using linear interpolation
5. Return the cleaned DataFrame sorted by date

This is a common data engineering task -- real-world data is messy.
"""

import pandas as pd
import numpy as np
from typing import Optional


def clean_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a sales DataFrame by handling missing values with multiple strategies.

    Args:
        df: DataFrame with columns [date, product, category, price, units_sold]
            May contain NaN values in any column except date.

    Returns:
        Cleaned DataFrame with no NaN values, sorted by date.

    Steps:
        1. Drop rows where more than half the columns are NaN
        2. Fill missing 'category' with 'Unknown'
        3. Fill missing 'price' with median price per category
        4. Interpolate missing 'units_sold' linearly
        5. Sort by date and reset index
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_clean_missing_data():
    """Test basic missing data cleanup."""
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10),
        'product': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
        'category': ['Electronics', 'Electronics', None, 'Clothing',
                      'Electronics', None, 'Clothing', 'Clothing', None, 'Electronics'],
        'price': [100.0, 200.0, np.nan, 50.0, 100.0, 200.0, np.nan, 50.0, 100.0, np.nan],
        'units_sold': [10, np.nan, 30, 40, np.nan, 60, 70, np.nan, 90, 100]
    })

    result = clean_missing_data(df)

    # No NaN values should remain
    assert result.isnull().sum().sum() == 0, "There should be no NaN values after cleaning"

    # All rows should be preserved (none have more than half NaN)
    assert len(result) == 10, f"Expected 10 rows, got {len(result)}"

    # Category NaN should be filled with 'Unknown'
    assert 'Unknown' in result['category'].values, "NaN categories should be filled with 'Unknown'"

    # Result should be sorted by date
    assert result['date'].is_monotonic_increasing, "Result should be sorted by date"

    print("PASS: Basic missing data cleanup works correctly")


def test_drop_mostly_null_rows():
    """Test that rows with more than half NaN values are dropped."""
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=5),
        'product': ['A', None, 'C', None, 'E'],
        'category': ['X', None, 'Z', None, 'X'],
        'price': [10.0, np.nan, 30.0, np.nan, 50.0],
        'units_sold': [1, np.nan, 3, np.nan, 5]
    })

    result = clean_missing_data(df)

    # Rows at index 1 and 3 have 4 out of 5 columns as NaN (product, category, price, units_sold)
    # That is more than half, so they should be dropped
    assert len(result) == 3, f"Expected 3 rows after dropping mostly-null rows, got {len(result)}"

    print("PASS: Mostly-null rows are correctly dropped")


def test_interpolation():
    """Test that units_sold interpolation works."""
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=5),
        'product': ['A', 'A', 'A', 'A', 'A'],
        'category': ['X', 'X', 'X', 'X', 'X'],
        'price': [10.0, 20.0, 30.0, 40.0, 50.0],
        'units_sold': [10.0, np.nan, 30.0, np.nan, 50.0]
    })

    result = clean_missing_data(df)

    # Linear interpolation: between 10 and 30 should give 20, between 30 and 50 should give 40
    assert result['units_sold'].iloc[1] == 20.0, f"Expected interpolated value 20.0, got {result['units_sold'].iloc[1]}"
    assert result['units_sold'].iloc[3] == 40.0, f"Expected interpolated value 40.0, got {result['units_sold'].iloc[3]}"

    print("PASS: Interpolation works correctly")


if __name__ == "__main__":
    test_clean_missing_data()
    test_drop_mostly_null_rows()
    test_interpolation()
    print("\nAll tests passed! Great job!")

# -*- coding: utf-8 -*-
"""
Problem: Reshape sales data using pivot_table, melt, and stack/unstack

Difficulty: Medium
Estimated Time: 15 minutes
Topics: pivot_table, melt, stack, unstack, reshaping

Given sales data in long format, perform various reshaping operations:
1. Create a pivot table showing total sales per product per region
2. Melt a wide-format DataFrame back into long format
3. Use stack/unstack to transform multi-level indexed data

These operations are critical for preparing data for reporting and visualization.
"""

import pandas as pd
import numpy as np
from typing import List


def create_pivot_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a pivot table showing total sales per product per region.

    Args:
        df: DataFrame with columns [date, product, region, sales, quantity]

    Returns:
        Pivot table with:
        - index: product
        - columns: region
        - values: sum of sales
        - Fill NaN with 0
        - Sorted by product name (index)
    """
    # TODO: Implement your solution here
    pass


def melt_wide_to_long(df: pd.DataFrame, id_cols: List[str], value_cols: List[str]) -> pd.DataFrame:
    """
    Convert a wide-format DataFrame to long format using melt.

    Args:
        df: Wide-format DataFrame
        id_cols: Columns to keep as identifiers
        value_cols: Columns to unpivot into rows

    Returns:
        Long-format DataFrame with columns from id_cols plus 'metric' and 'value'.
        The 'metric' column contains the former column names.
        The 'value' column contains the corresponding values.
        Sorted by the first id column, then by metric.
    """
    # TODO: Implement your solution here
    pass


def stack_unstack_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a DataFrame with a MultiIndex (product, region) and columns for each quarter,
    unstack the region level to create a hierarchical column index,
    then return the result.

    Args:
        df: DataFrame with MultiIndex (product, region) and quarterly sales columns
            e.g., columns = ['Q1', 'Q2', 'Q3', 'Q4']

    Returns:
        DataFrame with product as index and hierarchical columns (quarter, region).
        The unstacked level should be 'region'.
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_create_pivot_table():
    """Test pivot table creation."""
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=8),
        'product': ['Widget', 'Widget', 'Gadget', 'Gadget', 'Widget', 'Gadget', 'Widget', 'Gadget'],
        'region': ['North', 'South', 'North', 'South', 'North', 'South', 'South', 'North'],
        'sales': [100, 200, 150, 250, 300, 350, 400, 450],
        'quantity': [1, 2, 1, 3, 3, 4, 4, 5]
    })

    result = create_pivot_table(df)

    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"
    assert 'North' in result.columns, "Result should have 'North' column"
    assert 'South' in result.columns, "Result should have 'South' column"

    # Gadget North = 150 + 450 = 600
    assert result.loc['Gadget', 'North'] == 600, f"Gadget North should be 600, got {result.loc['Gadget', 'North']}"
    # Widget South = 200 + 400 = 600
    assert result.loc['Widget', 'South'] == 600, f"Widget South should be 600, got {result.loc['Widget', 'South']}"

    print("PASS: Pivot table created correctly")


def test_melt_wide_to_long():
    """Test melting wide format to long format."""
    wide_df = pd.DataFrame({
        'product': ['Widget', 'Gadget'],
        'Q1_sales': [1000, 1500],
        'Q2_sales': [1200, 1600],
        'Q3_sales': [1100, 1700]
    })

    result = melt_wide_to_long(
        wide_df,
        id_cols=['product'],
        value_cols=['Q1_sales', 'Q2_sales', 'Q3_sales']
    )

    assert len(result) == 6, f"Expected 6 rows, got {len(result)}"
    assert 'metric' in result.columns, "Result should have 'metric' column"
    assert 'value' in result.columns, "Result should have 'value' column"

    gadget_q1 = result[(result['product'] == 'Gadget') & (result['metric'] == 'Q1_sales')]['value'].values[0]
    assert gadget_q1 == 1500, f"Gadget Q1_sales should be 1500, got {gadget_q1}"

    print("PASS: Melt operation works correctly")


def test_stack_unstack_transform():
    """Test stack/unstack transformation."""
    index = pd.MultiIndex.from_tuples(
        [('Gadget', 'North'), ('Gadget', 'South'), ('Widget', 'North'), ('Widget', 'South')],
        names=['product', 'region']
    )
    df = pd.DataFrame({
        'Q1': [100, 200, 300, 400],
        'Q2': [150, 250, 350, 450]
    }, index=index)

    result = stack_unstack_transform(df)

    # After unstacking region, we should have product as index
    assert result.index.name == 'product', "Index should be 'product'"

    # Should have hierarchical columns
    assert isinstance(result.columns, pd.MultiIndex), "Columns should be a MultiIndex"

    # Check a value: Widget, Q1, South = 400
    assert result.loc['Widget', ('Q1', 'South')] == 400, \
        f"Widget Q1 South should be 400, got {result.loc['Widget', ('Q1', 'South')]}"

    print("PASS: Stack/unstack transformation works correctly")


if __name__ == "__main__":
    test_create_pivot_table()
    test_melt_wide_to_long()
    test_stack_unstack_transform()
    print("\nAll tests passed! Great job!")

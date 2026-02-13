# -*- coding: utf-8 -*-
"""
Problem: Merge multiple DataFrames with different join strategies

Difficulty: Medium
Estimated Time: 20 minutes
Topics: merge, join, concat, handling duplicates, join types

Given several related DataFrames (orders, products, customers, shipping),
perform various merge operations:
1. Inner join orders with products
2. Left join to preserve all orders even without matching products
3. Handle duplicate column names after merge
4. Multi-key merge with composite keys

Merging is arguably the most important pandas operation for data engineers.
"""

import pandas as pd
from typing import List


def inner_merge_orders_products(
    orders: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:
    """
    Inner merge orders with products on product_id.

    Args:
        orders: DataFrame with columns [order_id, customer_id, product_id, quantity, order_date]
        products: DataFrame with columns [product_id, product_name, price, category]

    Returns:
        Merged DataFrame containing only orders that have matching products.
        Include a calculated column 'total_amount' = quantity * price.
        Sort by order_id.
    """
    # TODO: Implement your solution here
    pass


def left_merge_with_nulls(
    orders: pd.DataFrame,
    customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Left merge orders with customers, keeping all orders.

    Args:
        orders: DataFrame with columns [order_id, customer_id, product_id, quantity]
        customers: DataFrame with columns [customer_id, customer_name, email, tier]

    Returns:
        Merged DataFrame with all orders. Where customer info is missing,
        fill customer_name with 'Unknown Customer' and tier with 'standard'.
        Sort by order_id.
    """
    # TODO: Implement your solution here
    pass


def multi_source_merge(
    orders: pd.DataFrame,
    products: pd.DataFrame,
    customers: pd.DataFrame,
    shipping: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge four DataFrames together to create a complete order view.

    Args:
        orders: [order_id, customer_id, product_id, quantity, order_date]
        products: [product_id, product_name, price]
        customers: [customer_id, customer_name, email]
        shipping: [order_id, shipping_date, carrier, tracking_number]

    Returns:
        Fully merged DataFrame with columns:
        [order_id, customer_name, product_name, quantity, price, total_amount,
         order_date, shipping_date, carrier]
        - total_amount = quantity * price
        - Use left joins from orders to preserve all orders
        - Sort by order_id
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def _make_test_data():
    """Create test DataFrames."""
    orders = pd.DataFrame({
        'order_id': [1, 2, 3, 4, 5],
        'customer_id': [101, 102, 103, 101, 999],
        'product_id': [201, 202, 201, 203, 201],
        'quantity': [2, 1, 3, 1, 5],
        'order_date': pd.date_range('2024-01-01', periods=5)
    })

    products = pd.DataFrame({
        'product_id': [201, 202, 203],
        'product_name': ['Laptop', 'Mouse', 'Keyboard'],
        'price': [1000.0, 25.0, 75.0],
        'category': ['Electronics', 'Accessories', 'Accessories']
    })

    customers = pd.DataFrame({
        'customer_id': [101, 102, 103],
        'customer_name': ['Alice', 'Bob', 'Charlie'],
        'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com'],
        'tier': ['premium', 'standard', 'premium']
    })

    shipping = pd.DataFrame({
        'order_id': [1, 2, 3, 4],
        'shipping_date': pd.date_range('2024-01-03', periods=4),
        'carrier': ['FedEx', 'UPS', 'FedEx', 'DHL'],
        'tracking_number': ['FX001', 'UP002', 'FX003', 'DH004']
    })

    return orders, products, customers, shipping


def test_inner_merge():
    """Test inner merge of orders and products."""
    orders, products, _, _ = _make_test_data()
    result = inner_merge_orders_products(orders, products)

    assert len(result) == 5, f"Expected 5 rows, got {len(result)}"
    assert 'total_amount' in result.columns, "Must have 'total_amount' column"
    assert 'product_name' in result.columns, "Must have 'product_name' column"

    # Order 1: 2 * 1000 = 2000
    row1 = result[result['order_id'] == 1].iloc[0]
    assert row1['total_amount'] == 2000.0, f"Order 1 total should be 2000, got {row1['total_amount']}"

    print("PASS: Inner merge works correctly")


def test_left_merge_with_nulls():
    """Test left merge preserving all orders."""
    orders, _, customers, _ = _make_test_data()
    result = left_merge_with_nulls(orders, customers)

    assert len(result) == 5, f"Expected 5 rows (all orders), got {len(result)}"

    # Order 5 has customer_id=999 which does not exist in customers
    unknown_row = result[result['order_id'] == 5].iloc[0]
    assert unknown_row['customer_name'] == 'Unknown Customer', \
        f"Missing customer should be 'Unknown Customer', got {unknown_row['customer_name']}"
    assert unknown_row['tier'] == 'standard', \
        f"Missing tier should be 'standard', got {unknown_row['tier']}"

    print("PASS: Left merge with null handling works correctly")


def test_multi_source_merge():
    """Test merging four DataFrames."""
    orders, products, customers, shipping = _make_test_data()
    result = multi_source_merge(orders, products, customers, shipping)

    assert len(result) == 5, f"Expected 5 rows (all orders), got {len(result)}"

    expected_cols = ['order_id', 'customer_name', 'product_name', 'quantity',
                     'price', 'total_amount', 'order_date', 'shipping_date', 'carrier']
    for col in expected_cols:
        assert col in result.columns, f"Missing column: {col}"

    # Order 5 has no shipping info
    row5 = result[result['order_id'] == 5].iloc[0]
    assert pd.isna(row5['carrier']), "Order 5 should have no carrier (NaN)"

    print("PASS: Multi-source merge works correctly")


if __name__ == "__main__":
    test_inner_merge()
    test_left_merge_with_nulls()
    test_multi_source_merge()
    print("\nAll tests passed! Great job!")

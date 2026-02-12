"""
Problem: Calculate top 5 customers by revenue from transactions

Difficulty: Medium
Estimated Time: 20 minutes
Topics: groupby, sorting, merging, filtering

Given two DataFrames:
- transactions: Contains transaction records
- customers: Contains customer information

Task:
1. Filter only 'completed' transactions
2. Calculate total revenue per customer
3. Merge with customer names
4. Return top 5 customers by revenue

Expected Output:
[
    {"customer_name": "Alice Johnson", "total_revenue": 15000.50},
    {"customer_name": "Bob Smith", "total_revenue": 12000.00},
    ...
]
"""

import pandas as pd
from typing import List, Dict


def top_customers_by_revenue(
    transactions: pd.DataFrame,
    customers: pd.DataFrame,
    top_n: int = 5
) -> List[Dict[str, any]]:
    """
    Calculate top N customers by revenue.

    Args:
        transactions: DataFrame with columns [id, customer_id, amount, status, date]
        customers: DataFrame with columns [id, name, email]
        top_n: Number of top customers to return

    Returns:
        List of dictionaries with customer_name and total_revenue
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_top_customers():
    """Test the top customers function."""
    # Sample data
    transactions = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6, 7, 8],
        'customer_id': [1, 1, 2, 2, 3, 3, 4, 4],
        'amount': [1000, 2000, 1500, 500, 3000, 2000, 800, 1200],
        'status': ['completed', 'completed', 'completed', 'failed',
                   'completed', 'completed', 'completed', 'completed'],
        'date': pd.date_range('2024-01-01', periods=8)
    })

    customers = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Martinez'],
        'email': ['alice@email.com', 'bob@email.com', 'charlie@email.com',
                  'diana@email.com', 'eve@email.com']
    })

    result = top_customers_by_revenue(transactions, customers, top_n=3)

    expected = [
        {'customer_name': 'Charlie Brown', 'total_revenue': 5000.0},
        {'customer_name': 'Alice Johnson', 'total_revenue': 3000.0},
        {'customer_name': 'Diana Prince', 'total_revenue': 2000.0}
    ]

    assert result == expected, f"Expected {expected}, got {result}"
    print("✅ Test passed!")
    print(f"✅ Top 3 customers by revenue:")
    for customer in result:
        print(f"   {customer['customer_name']}: ${customer['total_revenue']:,.2f}")


def test_edge_cases():
    """Test edge cases."""
    transactions = pd.DataFrame({
        'id': [1],
        'customer_id': [1],
        'amount': [1000],
        'status': ['failed'],
        'date': ['2024-01-01']
    })

    customers = pd.DataFrame({
        'id': [1],
        'name': ['Alice'],
        'email': ['alice@email.com']
    })

    result = top_customers_by_revenue(transactions, customers, top_n=5)
    assert result == [], f"Expected empty list for no completed transactions, got {result}"
    print("✅ Edge case test passed!")


if __name__ == "__main__":
    test_top_customers()
    test_edge_cases()
    print("\n✅ All tests passed! Great job!")

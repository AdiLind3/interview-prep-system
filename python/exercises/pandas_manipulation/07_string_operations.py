# -*- coding: utf-8 -*-
"""
Problem: Clean and extract information from text columns using pandas str accessor

Difficulty: Easy
Estimated Time: 15 minutes
Topics: str.extract, str.contains, str.replace, regex, string cleaning

Given a DataFrame of messy customer data:
1. Extract email domains
2. Clean phone numbers to a standard format
3. Parse full names into first and last
4. Filter rows based on string patterns

String operations are essential for data cleaning in ETL pipelines.
"""

import pandas as pd
from typing import List


def extract_email_domains(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the domain from email addresses.

    Args:
        df: DataFrame with an 'email' column containing email addresses.

    Returns:
        Original DataFrame with an additional 'domain' column.
        The domain is everything after the '@' sign, lowercased.
        If email is NaN, domain should also be NaN.
    """
    # TODO: Implement your solution here
    pass


def clean_phone_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize phone numbers to format: XXX-XXX-XXXX.

    Args:
        df: DataFrame with a 'phone' column containing phone numbers in various formats:
            - (555) 123-4567
            - 555.123.4567
            - 5551234567
            - 555-123-4567

    Returns:
        Original DataFrame with the 'phone' column cleaned.
        All phone numbers should be in format: XXX-XXX-XXXX.
        If phone is NaN, leave as NaN.
    """
    # TODO: Implement your solution here
    # Hint: Strip all non-digit characters first, then reformat
    pass


def parse_full_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split a 'full_name' column into 'first_name' and 'last_name'.

    Args:
        df: DataFrame with a 'full_name' column (e.g., "John Smith", "Jane Marie Doe").

    Returns:
        Original DataFrame with two new columns:
        - first_name: The first word
        - last_name: Everything after the first word (may contain middle names)
        Both columns should be stripped of leading/trailing whitespace.
    """
    # TODO: Implement your solution here
    pass


def filter_by_pattern(df: pd.DataFrame, column: str, pattern: str) -> pd.DataFrame:
    """
    Filter DataFrame rows where a column matches a regex pattern (case-insensitive).

    Args:
        df: Input DataFrame
        column: Column name to search in
        pattern: Regex pattern to match

    Returns:
        Filtered DataFrame containing only rows where the column matches the pattern.
        Reset the index.
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_extract_email_domains():
    """Test email domain extraction."""
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'email': ['alice@gmail.com', 'bob@Company.COM', 'charlie@yahoo.co.uk', None]
    })

    result = extract_email_domains(df)

    assert result.loc[0, 'domain'] == 'gmail.com', f"Expected 'gmail.com', got {result.loc[0, 'domain']}"
    assert result.loc[1, 'domain'] == 'company.com', f"Expected 'company.com', got {result.loc[1, 'domain']}"
    assert result.loc[2, 'domain'] == 'yahoo.co.uk', f"Expected 'yahoo.co.uk', got {result.loc[2, 'domain']}"
    assert pd.isna(result.loc[3, 'domain']), "NaN email should result in NaN domain"

    print("PASS: Email domain extraction works correctly")


def test_clean_phone_numbers():
    """Test phone number cleaning."""
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'phone': ['(555) 123-4567', '555.123.4567', '5551234567', '555-123-4567', None]
    })

    result = clean_phone_numbers(df)

    for i in range(4):
        assert result.loc[i, 'phone'] == '555-123-4567', \
            f"Row {i}: Expected '555-123-4567', got {result.loc[i, 'phone']}"

    assert pd.isna(result.loc[4, 'phone']), "NaN phone should remain NaN"

    print("PASS: Phone number cleaning works correctly")


def test_parse_full_names():
    """Test full name parsing."""
    df = pd.DataFrame({
        'full_name': ['John Smith', 'Jane Marie Doe', 'Alice Johnson']
    })

    result = parse_full_names(df)

    assert result.loc[0, 'first_name'] == 'John', f"Expected 'John', got {result.loc[0, 'first_name']}"
    assert result.loc[0, 'last_name'] == 'Smith', f"Expected 'Smith', got {result.loc[0, 'last_name']}"
    assert result.loc[1, 'first_name'] == 'Jane', f"Expected 'Jane', got {result.loc[1, 'first_name']}"
    assert result.loc[1, 'last_name'] == 'Marie Doe', f"Expected 'Marie Doe', got {result.loc[1, 'last_name']}"

    print("PASS: Full name parsing works correctly")


def test_filter_by_pattern():
    """Test pattern-based filtering."""
    df = pd.DataFrame({
        'product': ['Widget Pro', 'Gadget Plus', 'Widget Basic', 'Super Gadget', 'Tool Kit'],
        'price': [100, 200, 50, 300, 75]
    })

    result = filter_by_pattern(df, 'product', r'widget')

    assert len(result) == 2, f"Expected 2 rows matching 'widget', got {len(result)}"
    assert all('Widget' in name for name in result['product'].values), "All results should contain 'Widget'"

    print("PASS: Pattern filtering works correctly")


if __name__ == "__main__":
    test_extract_email_domains()
    test_clean_phone_numbers()
    test_parse_full_names()
    test_filter_by_pattern()
    print("\nAll tests passed! Great job!")

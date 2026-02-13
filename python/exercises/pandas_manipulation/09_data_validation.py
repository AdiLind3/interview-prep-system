# -*- coding: utf-8 -*-
"""
Problem: Validate DataFrame schema, check constraints, and find anomalies

Difficulty: Medium
Estimated Time: 20 minutes
Topics: data validation, schema checking, anomaly detection, constraints

Given a DataFrame of transaction data:
1. Validate that the schema matches expected column names and types
2. Check business rule constraints (e.g., positive amounts, valid dates)
3. Identify anomalous rows that violate rules
4. Generate a validation report

Data validation is a critical step in any ETL pipeline before loading data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of a validation check."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    invalid_row_count: int = 0


def validate_schema(
    df: pd.DataFrame,
    expected_columns: Dict[str, str]
) -> ValidationResult:
    """
    Validate that a DataFrame has the expected columns and compatible types.

    Args:
        df: DataFrame to validate
        expected_columns: Dict mapping column_name -> expected dtype string.
            Supported dtype strings: 'int64', 'float64', 'object', 'datetime64', 'bool'

    Returns:
        ValidationResult with:
        - is_valid: True if all columns exist with correct types
        - errors: List of error messages for missing columns or type mismatches

    Notes:
        - For datetime columns, accept any datetime64 variant (e.g., datetime64[ns])
        - For numeric checks, 'int64' should also accept 'Int64' (nullable integer)
    """
    # TODO: Implement your solution here
    pass


def check_constraints(df: pd.DataFrame) -> ValidationResult:
    """
    Check business rule constraints on a transactions DataFrame.

    Args:
        df: DataFrame with columns [transaction_id, amount, date, status, customer_id]

    Returns:
        ValidationResult with:
        - is_valid: True if no constraint violations found
        - errors: List of constraint violation descriptions
        - invalid_row_count: Number of rows with at least one violation

    Constraints to check:
        1. 'amount' must be positive (> 0)
        2. 'transaction_id' must be unique (no duplicates)
        3. 'status' must be one of: 'completed', 'pending', 'failed', 'refunded'
        4. 'customer_id' must not be null
        5. 'date' must not be in the future (use pd.Timestamp.now() as reference)
    """
    # TODO: Implement your solution here
    pass


def find_anomalies(
    df: pd.DataFrame,
    column: str,
    method: str = 'zscore',
    threshold: float = 2.0
) -> pd.DataFrame:
    """
    Find anomalous rows based on a numeric column.

    Args:
        df: Input DataFrame
        column: Numeric column to check for anomalies
        method: Detection method - 'zscore' or 'iqr'
        threshold: For zscore method, the number of standard deviations.
                   For iqr method, the IQR multiplier (typically 1.5).

    Returns:
        DataFrame containing only the anomalous rows.

    Methods:
        - zscore: Flag rows where |z-score| > threshold
        - iqr: Flag rows outside [Q1 - threshold*IQR, Q3 + threshold*IQR]
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_validate_schema():
    """Test schema validation."""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'amount': [100.0, 200.0, 300.0],
        'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03'])
    })

    # Valid schema
    result = validate_schema(df, {
        'id': 'int64',
        'name': 'object',
        'amount': 'float64',
        'date': 'datetime64'
    })
    assert result.is_valid, f"Schema should be valid, errors: {result.errors}"

    # Invalid schema (missing column)
    result = validate_schema(df, {
        'id': 'int64',
        'name': 'object',
        'amount': 'float64',
        'date': 'datetime64',
        'missing_col': 'object'
    })
    assert not result.is_valid, "Schema should be invalid when column is missing"
    assert any('missing_col' in err for err in result.errors), "Error should mention missing column"

    print("PASS: Schema validation works correctly")


def test_check_constraints():
    """Test constraint checking."""
    df = pd.DataFrame({
        'transaction_id': [1, 2, 3, 3, 5],
        'amount': [100.0, -50.0, 200.0, 300.0, 0.0],
        'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']),
        'status': ['completed', 'pending', 'invalid_status', 'failed', 'completed'],
        'customer_id': [101, 102, None, 104, 105]
    })

    result = check_constraints(df)

    assert not result.is_valid, "Constraints should be violated"
    assert result.invalid_row_count > 0, "Should have invalid rows"

    # Check that specific violations are detected
    errors_text = ' '.join(result.errors)
    assert 'amount' in errors_text.lower() or 'positive' in errors_text.lower(), \
        "Should detect negative/zero amounts"
    assert 'duplicate' in errors_text.lower() or 'unique' in errors_text.lower(), \
        "Should detect duplicate transaction_ids"

    print("PASS: Constraint checking works correctly")


def test_find_anomalies_zscore():
    """Test anomaly detection with z-score method."""
    np.random.seed(42)
    normal_data = np.random.normal(100, 10, 100)
    # Inject clear anomalies
    anomaly_data = np.concatenate([normal_data, [200, 5, 250]])

    df = pd.DataFrame({
        'value': anomaly_data,
        'label': [f'item_{i}' for i in range(103)]
    })

    result = find_anomalies(df, 'value', method='zscore', threshold=2.0)

    # Should detect the injected anomalies
    assert len(result) >= 2, f"Expected at least 2 anomalies, got {len(result)}"
    assert 200 in result['value'].values or 250 in result['value'].values, \
        "Should detect the extreme high values"

    print("PASS: Z-score anomaly detection works correctly")


def test_find_anomalies_iqr():
    """Test anomaly detection with IQR method."""
    np.random.seed(42)
    normal_data = np.random.normal(100, 10, 100)
    anomaly_data = np.concatenate([normal_data, [200, 5]])

    df = pd.DataFrame({
        'value': anomaly_data,
        'label': [f'item_{i}' for i in range(102)]
    })

    result = find_anomalies(df, 'value', method='iqr', threshold=1.5)

    assert len(result) >= 2, f"Expected at least 2 anomalies with IQR, got {len(result)}"

    print("PASS: IQR anomaly detection works correctly")


if __name__ == "__main__":
    test_validate_schema()
    test_check_constraints()
    test_find_anomalies_zscore()
    test_find_anomalies_iqr()
    print("\nAll tests passed! Great job!")

# -*- coding: utf-8 -*-
"""
Problem: Build a mini ETL pipeline that extracts, transforms, validates, and loads data

Difficulty: Hard
Estimated Time: 30 minutes
Topics: ETL, data pipeline, transformation, validation, pandas

Build a complete ETL pipeline class that:
1. Extracts data from a source (simulated as a DataFrame)
2. Transforms: cleans, enriches, and aggregates
3. Validates the output against business rules
4. Loads to a destination (returns the final DataFrame)

This exercise simulates what you would build with tools like Airflow, dbt, or custom scripts.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Result of an ETL pipeline run."""
    success: bool
    rows_input: int
    rows_output: int
    rows_dropped: int
    validation_errors: List[str] = field(default_factory=list)
    data: Optional[pd.DataFrame] = None


class SalesETLPipeline:
    """
    A mini ETL pipeline for processing raw sales data.

    The pipeline processes raw transaction data through these stages:
    1. Extract: Accept raw data
    2. Clean: Handle missing values, fix types, remove invalid rows
    3. Enrich: Add calculated columns (total, category tier)
    4. Aggregate: Summarize by customer
    5. Validate: Check output quality
    """

    def __init__(self, min_order_amount: float = 0.0, valid_statuses: Optional[List[str]] = None):
        """
        Initialize pipeline with configuration.

        Args:
            min_order_amount: Minimum order amount to keep (filter out smaller)
            valid_statuses: List of valid order statuses. Defaults to ['completed', 'pending'].
        """
        self.min_order_amount = min_order_amount
        self.valid_statuses = valid_statuses or ['completed', 'pending']

    def extract(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract stage: Accept raw data and make a copy.

        Args:
            raw_data: Raw DataFrame with columns:
                [order_id, customer_id, product, quantity, unit_price, status, order_date]

        Returns:
            Copy of the input DataFrame.
        """
        # TODO: Implement extraction (make a copy, log row count)
        pass

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean stage: Handle missing values and fix data types.

        Steps:
            1. Drop rows where order_id or customer_id is null
            2. Fill missing 'status' with 'pending'
            3. Fill missing 'quantity' with 1
            4. Fill missing 'unit_price' with 0.0
            5. Ensure 'order_date' is datetime type
            6. Remove duplicate order_ids (keep first)

        Args:
            df: Extracted DataFrame

        Returns:
            Cleaned DataFrame
        """
        # TODO: Implement cleaning logic
        pass

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich stage: Add calculated columns.

        Steps:
            1. Add 'total_amount' = quantity * unit_price
            2. Filter to only valid statuses (self.valid_statuses)
            3. Filter out orders below self.min_order_amount
            4. Add 'order_month' column (YYYY-MM string format)

        Args:
            df: Cleaned DataFrame

        Returns:
            Enriched DataFrame
        """
        # TODO: Implement enrichment logic
        pass

    def aggregate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate stage: Summarize by customer.

        Args:
            df: Enriched DataFrame

        Returns:
            DataFrame with one row per customer_id containing:
            - customer_id
            - total_orders: count of orders
            - total_revenue: sum of total_amount
            - avg_order_value: mean of total_amount, rounded to 2 decimals
            - first_order: min order_date
            - last_order: max order_date
            Sorted by total_revenue descending.
        """
        # TODO: Implement aggregation logic
        pass

    def validate(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate stage: Check output data quality.

        Checks:
            1. DataFrame is not empty
            2. No null values in customer_id
            3. All total_revenue values are >= 0
            4. All total_orders values are > 0

        Args:
            df: Aggregated DataFrame

        Returns:
            Tuple of (is_valid, list_of_error_messages)
        """
        # TODO: Implement validation logic
        pass

    def run(self, raw_data: pd.DataFrame) -> PipelineResult:
        """
        Execute the full ETL pipeline.

        Args:
            raw_data: Raw input DataFrame

        Returns:
            PipelineResult with success status, metrics, and output data.
        """
        # TODO: Implement the full pipeline by calling each stage
        # Use try/except to handle errors gracefully
        # Log progress at each stage
        pass


# ============ TESTS (DO NOT MODIFY) ============

def _make_raw_data() -> pd.DataFrame:
    """Create realistic raw test data with quality issues."""
    return pd.DataFrame({
        'order_id': [1, 2, 3, 4, 5, 6, 7, 8, 8, None],
        'customer_id': [101, 102, 101, 103, 102, None, 101, 103, 103, 104],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop',
                     'Mouse', 'Headset', 'Webcam', 'Webcam', 'Cable'],
        'quantity': [1, 2, 1, None, 1, 3, 2, 1, 1, 5],
        'unit_price': [1000.0, 25.0, 75.0, 300.0, 1000.0, None, 50.0, 80.0, 80.0, 10.0],
        'status': ['completed', 'completed', 'pending', 'completed', 'failed',
                   'completed', 'completed', None, 'completed', 'completed'],
        'order_date': pd.to_datetime([
            '2024-01-15', '2024-01-20', '2024-02-01', '2024-02-10', '2024-02-15',
            '2024-03-01', '2024-03-10', '2024-03-15', '2024-03-15', '2024-03-20'
        ])
    })


def test_full_pipeline():
    """Test the complete ETL pipeline."""
    raw_data = _make_raw_data()
    pipeline = SalesETLPipeline(min_order_amount=0.0)
    result = pipeline.run(raw_data)

    assert result.success, f"Pipeline should succeed, errors: {result.validation_errors}"
    assert result.rows_input == 10, f"Expected 10 input rows, got {result.rows_input}"
    assert result.data is not None, "Pipeline should return data"
    assert 'total_revenue' in result.data.columns, "Output should have 'total_revenue'"
    assert 'total_orders' in result.data.columns, "Output should have 'total_orders'"

    # Should have dropped: null order_id (row 10), null customer_id (row 6), duplicate order 8
    # Then filtered out 'failed' status (order 5)
    assert result.rows_output > 0, "Should have output rows"

    print("PASS: Full ETL pipeline works correctly")


def test_pipeline_with_filter():
    """Test pipeline with minimum order amount filter."""
    raw_data = _make_raw_data()
    pipeline = SalesETLPipeline(min_order_amount=100.0)
    result = pipeline.run(raw_data)

    assert result.success, f"Pipeline should succeed, errors: {result.validation_errors}"

    # All remaining orders should have total_amount >= 100
    if result.data is not None and len(result.data) > 0:
        # The aggregate output has total_revenue, not individual amounts
        # But we can check that the pipeline completed
        assert result.rows_output <= result.rows_input, "Should have fewer or equal output rows"

    print("PASS: Pipeline with filter works correctly")


def test_pipeline_empty_input():
    """Test pipeline with empty DataFrame."""
    empty_df = pd.DataFrame({
        'order_id': pd.Series(dtype='float64'),
        'customer_id': pd.Series(dtype='float64'),
        'product': pd.Series(dtype='str'),
        'quantity': pd.Series(dtype='float64'),
        'unit_price': pd.Series(dtype='float64'),
        'status': pd.Series(dtype='str'),
        'order_date': pd.Series(dtype='datetime64[ns]')
    })

    pipeline = SalesETLPipeline()
    result = pipeline.run(empty_df)

    assert not result.success, "Pipeline should fail on empty input"
    assert result.rows_input == 0, "Should report 0 input rows"

    print("PASS: Pipeline handles empty input correctly")


def test_individual_stages():
    """Test individual pipeline stages."""
    raw_data = _make_raw_data()
    pipeline = SalesETLPipeline()

    # Test extract
    extracted = pipeline.extract(raw_data)
    assert len(extracted) == len(raw_data), "Extract should preserve all rows"

    # Test clean
    cleaned = pipeline.clean(extracted)
    assert cleaned['order_id'].isnull().sum() == 0, "Clean should remove null order_ids"
    assert cleaned['order_id'].duplicated().sum() == 0, "Clean should remove duplicate order_ids"

    # Test enrich
    enriched = pipeline.enrich(cleaned)
    assert 'total_amount' in enriched.columns, "Enrich should add total_amount"
    assert 'order_month' in enriched.columns, "Enrich should add order_month"

    print("PASS: Individual pipeline stages work correctly")


if __name__ == "__main__":
    test_full_pipeline()
    test_pipeline_with_filter()
    test_pipeline_empty_input()
    test_individual_stages()
    print("\nAll tests passed! Great job!")

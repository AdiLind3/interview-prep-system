# -*- coding: utf-8 -*-
"""
Problem: Process data in configurable batches with progress tracking

Difficulty: Medium
Estimated Time: 20 minutes
Topics: batch processing, generators, progress tracking, error handling

Batch processing is fundamental to data engineering. Whether processing
millions of database rows, API calls, or file records, you need to
handle data in manageable chunks.

Tasks:
1. Process items in configurable batch sizes
2. Track progress and statistics
3. Handle errors gracefully (skip bad records, log them)
4. Support different processing modes
"""

import logging
import time
from typing import List, Dict, Any, Callable, Optional, Iterator, Tuple
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class BatchResult:
    """Result of processing a single batch."""
    batch_number: int
    total_items: int
    successful: int
    failed: int
    errors: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ProcessingReport:
    """Overall processing report."""
    total_items: int
    total_batches: int
    total_successful: int
    total_failed: int
    batch_results: List[BatchResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Return success rate as a percentage, rounded to 2 decimals."""
        if self.total_items == 0:
            return 0.0
        return round((self.total_successful / self.total_items) * 100, 2)


def create_batches(items: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Split items into batches of specified size.

    Args:
        items: List of items to split
        batch_size: Maximum items per batch (must be > 0)

    Returns:
        List of batches (each batch is a list).

    Raises:
        ValueError: If batch_size is less than 1.
    """
    # TODO: Implement your solution here
    pass


def process_batch(
    batch: List[Dict[str, Any]],
    processor: Callable[[Dict[str, Any]], Dict[str, Any]],
    batch_number: int
) -> BatchResult:
    """
    Process a single batch of records, handling errors per-record.

    Args:
        batch: List of record dictionaries
        processor: Function that takes a record and returns the processed record.
                   May raise an exception for invalid records.
        batch_number: The batch number (for reporting)

    Returns:
        BatchResult with counts and error details.
        Each error entry should have: {'record': <original record>, 'error': <error message>}
    """
    # TODO: Implement your solution here
    pass


def process_all(
    items: List[Dict[str, Any]],
    processor: Callable[[Dict[str, Any]], Dict[str, Any]],
    batch_size: int = 10,
    on_batch_complete: Optional[Callable[[BatchResult], None]] = None
) -> ProcessingReport:
    """
    Process all items in batches with full reporting.

    Args:
        items: List of record dictionaries to process
        processor: Function to apply to each record
        batch_size: Records per batch
        on_batch_complete: Optional callback called after each batch completes

    Returns:
        Complete ProcessingReport with all batch results.
    """
    # TODO: Implement your solution here
    pass


def make_processor_with_validation(
    required_fields: List[str],
    transform_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Create a processor function with built-in validation.

    Args:
        required_fields: Fields that must be present and non-None
        transform_fn: Optional transformation to apply after validation

    Returns:
        A processor function that validates then transforms records.
        Raises ValueError if validation fails.
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_create_batches():
    """Test batch creation."""
    items = list(range(10))

    batches = create_batches(items, batch_size=3)
    assert len(batches) == 4, f"Expected 4 batches, got {len(batches)}"
    assert batches[0] == [0, 1, 2], f"First batch: {batches[0]}"
    assert batches[-1] == [9], f"Last batch: {batches[-1]}"

    # Edge case: batch_size larger than items
    batches_big = create_batches(items, batch_size=20)
    assert len(batches_big) == 1, f"Expected 1 batch, got {len(batches_big)}"

    # Edge case: empty list
    batches_empty = create_batches([], batch_size=5)
    assert len(batches_empty) == 0, f"Expected 0 batches, got {len(batches_empty)}"

    # Edge case: invalid batch_size
    try:
        create_batches(items, batch_size=0)
        assert False, "Should raise ValueError for batch_size=0"
    except ValueError:
        pass

    print("PASS: Batch creation works correctly")


def test_process_batch():
    """Test single batch processing."""
    def simple_processor(record):
        if record.get('value', 0) < 0:
            raise ValueError("Negative value not allowed")
        return {**record, 'processed': True}

    batch = [
        {'id': 1, 'value': 10},
        {'id': 2, 'value': -5},
        {'id': 3, 'value': 20}
    ]

    result = process_batch(batch, simple_processor, batch_number=1)

    assert result.total_items == 3, f"Total items: {result.total_items}"
    assert result.successful == 2, f"Successful: {result.successful}"
    assert result.failed == 1, f"Failed: {result.failed}"
    assert len(result.errors) == 1, f"Errors: {len(result.errors)}"

    print("PASS: Single batch processing works correctly")


def test_process_all():
    """Test full batch processing."""
    def processor(record):
        if record.get('value') is None:
            raise ValueError("Missing value")
        return {**record, 'doubled': record['value'] * 2}

    items = [
        {'id': 1, 'value': 10},
        {'id': 2, 'value': 20},
        {'id': 3, 'value': None},
        {'id': 4, 'value': 40},
        {'id': 5, 'value': 50}
    ]

    batch_callbacks = []
    report = process_all(
        items, processor, batch_size=2,
        on_batch_complete=lambda r: batch_callbacks.append(r.batch_number)
    )

    assert report.total_items == 5, f"Total items: {report.total_items}"
    assert report.total_successful == 4, f"Successful: {report.total_successful}"
    assert report.total_failed == 1, f"Failed: {report.total_failed}"
    assert report.total_batches == 3, f"Batches: {report.total_batches}"
    assert report.success_rate == 80.0, f"Success rate: {report.success_rate}"
    assert len(batch_callbacks) == 3, f"Callbacks: {len(batch_callbacks)}"

    print("PASS: Full batch processing works correctly")


def test_processor_with_validation():
    """Test processor factory with validation."""
    processor = make_processor_with_validation(
        required_fields=['name', 'email'],
        transform_fn=lambda r: {**r, 'name': r['name'].upper()}
    )

    # Valid record
    result = processor({'name': 'alice', 'email': 'a@b.com', 'age': 30})
    assert result['name'] == 'ALICE', f"Name should be uppercased, got {result['name']}"

    # Invalid record (missing field)
    try:
        processor({'name': 'bob'})
        assert False, "Should raise ValueError for missing email"
    except ValueError:
        pass

    # Invalid record (None value)
    try:
        processor({'name': 'charlie', 'email': None})
        assert False, "Should raise ValueError for None email"
    except ValueError:
        pass

    print("PASS: Processor with validation works correctly")


if __name__ == "__main__":
    test_create_batches()
    test_process_batch()
    test_process_all()
    test_processor_with_validation()
    print("\nAll tests passed! Great job!")

# -*- coding: utf-8 -*-
"""
Problem: Process CSV data, transform it, and output as JSON (with chunked processing)

Difficulty: Medium
Estimated Time: 20 minutes
Topics: CSV, JSON, chunked processing, data transformation, file I/O

In data engineering, you frequently need to convert between formats.
This exercise simulates processing large CSV files in chunks and
outputting structured JSON.

Tasks:
1. Process records in chunks (memory-efficient)
2. Transform and clean each record
3. Output as JSON with proper structure
"""

import json
import logging
from typing import List, Dict, Any, Iterator, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def chunk_records(records: List[Dict[str, Any]], chunk_size: int) -> Iterator[List[Dict[str, Any]]]:
    """
    Split a list of records into chunks of specified size.

    Args:
        records: List of record dictionaries
        chunk_size: Maximum records per chunk

    Yields:
        Lists of records, each with at most chunk_size elements.
    """
    # TODO: Implement as a generator using yield
    pass


def transform_record(record: Dict[str, Any], field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """
    Transform a single record by renaming fields and cleaning values.

    Args:
        record: Input record dictionary
        field_mapping: Dict mapping old_field_name -> new_field_name.
                       Fields not in the mapping are dropped.

    Returns:
        Transformed record with:
        - Fields renamed according to field_mapping
        - String values stripped of leading/trailing whitespace
        - Empty string values converted to None
        - Numeric strings converted to float where possible

    Example:
        record = {'first_name': ' Alice ', 'age_str': '30', 'junk': 'x'}
        field_mapping = {'first_name': 'name', 'age_str': 'age'}
        Returns: {'name': 'Alice', 'age': 30.0}
    """
    # TODO: Implement your solution here
    pass


def process_and_convert(
    records: List[Dict[str, Any]],
    field_mapping: Dict[str, str],
    chunk_size: int = 100,
    filter_fn: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Process records in chunks, transform them, and return a JSON-compatible structure.

    Args:
        records: List of raw record dictionaries
        field_mapping: Field name mapping for transformation
        chunk_size: Number of records to process per chunk
        filter_fn: Optional callable that takes a record and returns True to keep it.
                   Applied after transformation.

    Returns:
        Dictionary with structure:
        {
            'metadata': {
                'total_input': int,
                'total_output': int,
                'chunks_processed': int
            },
            'records': List[Dict]  -- the transformed and filtered records
        }
    """
    # TODO: Implement your solution here
    pass


def records_to_json_string(data: Dict[str, Any], indent: int = 2) -> str:
    """
    Convert the processed data structure to a formatted JSON string.

    Args:
        data: Dictionary with 'metadata' and 'records' keys
        indent: JSON indentation level

    Returns:
        JSON string with UTF-8 encoding support (ensure_ascii=False).
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_chunk_records():
    """Test record chunking."""
    records = [{'id': i} for i in range(7)]
    chunks = list(chunk_records(records, chunk_size=3))

    assert len(chunks) == 3, f"Expected 3 chunks, got {len(chunks)}"
    assert len(chunks[0]) == 3, f"First chunk should have 3 records"
    assert len(chunks[1]) == 3, f"Second chunk should have 3 records"
    assert len(chunks[2]) == 1, f"Third chunk should have 1 record"

    print("PASS: Record chunking works correctly")


def test_transform_record():
    """Test record transformation."""
    record = {
        'first_name': '  Alice  ',
        'last_name': 'Smith',
        'age_str': '30',
        'salary_str': '75000.50',
        'empty_field': '',
        'junk_field': 'should be dropped'
    }
    mapping = {
        'first_name': 'name',
        'last_name': 'surname',
        'age_str': 'age',
        'salary_str': 'salary',
        'empty_field': 'notes'
    }

    result = transform_record(record, mapping)

    assert result['name'] == 'Alice', f"Name should be stripped, got '{result['name']}'"
    assert result['age'] == 30.0, f"Age should be numeric, got {result['age']}"
    assert result['salary'] == 75000.50, f"Salary should be numeric, got {result['salary']}"
    assert result['notes'] is None, f"Empty string should be None, got {result['notes']}"
    assert 'junk_field' not in result, "Unmapped fields should be dropped"

    print("PASS: Record transformation works correctly")


def test_process_and_convert():
    """Test full processing pipeline."""
    records = [
        {'name': ' Alice ', 'dept': 'Engineering', 'salary': '120000'},
        {'name': ' Bob ', 'dept': 'Marketing', 'salary': '90000'},
        {'name': ' Charlie ', 'dept': 'Engineering', 'salary': '110000'},
        {'name': '', 'dept': 'Sales', 'salary': '80000'},
        {'name': ' Eve ', 'dept': 'Engineering', 'salary': '95000'}
    ]
    mapping = {'name': 'employee_name', 'dept': 'department', 'salary': 'annual_salary'}

    result = process_and_convert(records, mapping, chunk_size=2)

    assert result['metadata']['total_input'] == 5, f"Total input: {result['metadata']['total_input']}"
    assert result['metadata']['total_output'] == 5, f"Total output: {result['metadata']['total_output']}"
    assert result['metadata']['chunks_processed'] == 3, f"Chunks: {result['metadata']['chunks_processed']}"
    assert len(result['records']) == 5, f"Records count: {len(result['records'])}"

    # Test with filter
    result_filtered = process_and_convert(
        records, mapping, chunk_size=2,
        filter_fn=lambda r: r.get('annual_salary') is not None and r['annual_salary'] >= 100000
    )
    assert result_filtered['metadata']['total_output'] == 2, \
        f"Filtered output: {result_filtered['metadata']['total_output']}"

    print("PASS: Full processing pipeline works correctly")


def test_json_output():
    """Test JSON string output."""
    data = {
        'metadata': {'total_input': 1, 'total_output': 1, 'chunks_processed': 1},
        'records': [{'name': 'Alice', 'salary': 100000.0}]
    }

    json_str = records_to_json_string(data)
    parsed = json.loads(json_str)

    assert parsed == data, f"JSON round-trip failed"
    assert '\n' in json_str, "JSON should be indented (contain newlines)"

    print("PASS: JSON output works correctly")


if __name__ == "__main__":
    test_chunk_records()
    test_transform_record()
    test_process_and_convert()
    test_json_output()
    print("\nAll tests passed! Great job!")

# -*- coding: utf-8 -*-
"""
Problem: Deduplicate records and find duplicates using hash-based approaches

Difficulty: Medium
Estimated Time: 15 minutes
Topics: hashing, deduplication, dict-based lookups, data quality

In data engineering, deduplication is one of the most common operations.
These exercises use hash-based approaches for efficient duplicate detection.

Tasks:
1. Find duplicate rows based on content hashing
2. Merge duplicate records with conflict resolution
3. Implement a fuzzy dedup using normalized keys
"""

import hashlib
from typing import List, Dict, Any, Tuple, Callable, Optional


def find_duplicate_groups(
    records: List[Dict[str, Any]],
    key_fields: List[str]
) -> Dict[str, List[int]]:
    """
    Group records by their key fields and identify duplicate groups.

    Args:
        records: List of record dictionaries
        key_fields: Fields that define uniqueness

    Returns:
        Dictionary mapping a hash string of the key fields to a list of
        indices (positions in the original list) where that key appears.
        Only include groups that have more than one record (actual duplicates).

    Example:
        records = [{'id': 1, 'v': 'a'}, {'id': 2, 'v': 'b'}, {'id': 1, 'v': 'c'}]
        find_duplicate_groups(records, ['id'])
        -> {'<hash_of_id=1>': [0, 2]}
    """
    # TODO: Implement your solution here
    # Hint: Create a string key from the key_fields, hash it, and track indices
    pass


def merge_duplicates(
    records: List[Dict[str, Any]],
    key_fields: List[str],
    merge_strategy: str = 'first'
) -> List[Dict[str, Any]]:
    """
    Merge duplicate records using specified strategy.

    Args:
        records: List of record dictionaries
        key_fields: Fields that define uniqueness
        merge_strategy: How to resolve conflicts for non-key fields:
            - 'first': Keep values from the first occurrence
            - 'last': Keep values from the last occurrence
            - 'combine': For conflicting values, create a list of unique values

    Returns:
        Deduplicated list of records. Order follows first occurrence of each key.
    """
    # TODO: Implement your solution here
    pass


def normalize_and_dedup(
    records: List[Dict[str, Any]],
    key_field: str,
    normalizer: Optional[Callable[[str], str]] = None
) -> Tuple[List[Dict[str, Any]], List[Tuple[int, int]]]:
    """
    Normalize a key field and deduplicate based on the normalized value.

    This handles cases like "John Smith" vs "john smith" vs "JOHN SMITH".

    Args:
        records: List of record dictionaries
        key_field: The field to normalize and dedup on
        normalizer: A function that normalizes a string value.
                    If None, use default: lowercase and strip whitespace.

    Returns:
        Tuple of:
        - Deduplicated records (keep first occurrence)
        - List of (kept_index, removed_index) pairs showing which records were merged
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_find_duplicate_groups():
    """Test finding duplicate groups."""
    records = [
        {'name': 'Alice', 'dept': 'eng', 'salary': 100},
        {'name': 'Bob', 'dept': 'sales', 'salary': 90},
        {'name': 'Alice', 'dept': 'eng', 'salary': 110},
        {'name': 'Charlie', 'dept': 'eng', 'salary': 95},
        {'name': 'Bob', 'dept': 'sales', 'salary': 92}
    ]

    result = find_duplicate_groups(records, ['name', 'dept'])

    # Should find 2 duplicate groups
    assert len(result) == 2, f"Expected 2 duplicate groups, got {len(result)}"

    # Check that each group has 2 records
    for key, indices in result.items():
        assert len(indices) == 2, f"Group {key} should have 2 records, got {len(indices)}"

    print("PASS: Duplicate group finding works correctly")


def test_merge_duplicates_first():
    """Test merging duplicates with 'first' strategy."""
    records = [
        {'id': 1, 'name': 'Alice', 'score': 90},
        {'id': 2, 'name': 'Bob', 'score': 85},
        {'id': 1, 'name': 'Alice', 'score': 95}
    ]

    result = merge_duplicates(records, ['id'], merge_strategy='first')
    assert len(result) == 2, f"Expected 2 records, got {len(result)}"

    rec1 = [r for r in result if r['id'] == 1][0]
    assert rec1['score'] == 90, f"First strategy should keep score=90, got {rec1['score']}"

    print("PASS: Merge with 'first' strategy works correctly")


def test_merge_duplicates_last():
    """Test merging duplicates with 'last' strategy."""
    records = [
        {'id': 1, 'name': 'Alice', 'score': 90},
        {'id': 2, 'name': 'Bob', 'score': 85},
        {'id': 1, 'name': 'Alice', 'score': 95}
    ]

    result = merge_duplicates(records, ['id'], merge_strategy='last')
    assert len(result) == 2, f"Expected 2 records, got {len(result)}"

    rec1 = [r for r in result if r['id'] == 1][0]
    assert rec1['score'] == 95, f"Last strategy should keep score=95, got {rec1['score']}"

    print("PASS: Merge with 'last' strategy works correctly")


def test_merge_duplicates_combine():
    """Test merging duplicates with 'combine' strategy."""
    records = [
        {'id': 1, 'name': 'Alice', 'tag': 'python'},
        {'id': 1, 'name': 'Alice', 'tag': 'sql'},
        {'id': 2, 'name': 'Bob', 'tag': 'java'}
    ]

    result = merge_duplicates(records, ['id'], merge_strategy='combine')
    assert len(result) == 2, f"Expected 2 records, got {len(result)}"

    rec1 = [r for r in result if r['id'] == 1][0]
    # 'tag' should be a list of unique values since they differ
    assert isinstance(rec1['tag'], list), f"Combined tag should be a list, got {type(rec1['tag'])}"
    assert set(rec1['tag']) == {'python', 'sql'}, f"Combined tags: {rec1['tag']}"

    # 'name' is the same in both, so it should stay as a string
    assert rec1['name'] == 'Alice', f"Same values should not become a list, got {rec1['name']}"

    print("PASS: Merge with 'combine' strategy works correctly")


def test_normalize_and_dedup():
    """Test normalization-based deduplication."""
    records = [
        {'name': 'John Smith', 'email': 'john@a.com'},
        {'name': 'JOHN SMITH', 'email': 'john@b.com'},
        {'name': 'jane doe', 'email': 'jane@a.com'},
        {'name': '  John Smith  ', 'email': 'john@c.com'}
    ]

    deduped, merge_pairs = normalize_and_dedup(records, 'name')

    assert len(deduped) == 2, f"Expected 2 unique records, got {len(deduped)}"
    assert deduped[0]['name'] == 'John Smith', "Should keep first occurrence"
    assert len(merge_pairs) == 2, f"Expected 2 merge pairs, got {len(merge_pairs)}"

    print("PASS: Normalize and dedup works correctly")


if __name__ == "__main__":
    test_find_duplicate_groups()
    test_merge_duplicates_first()
    test_merge_duplicates_last()
    test_merge_duplicates_combine()
    test_normalize_and_dedup()
    print("\nAll tests passed! Great job!")

# -*- coding: utf-8 -*-
"""
Problem: Use set operations for data deduplication and comparison

Difficulty: Easy
Estimated Time: 10 minutes
Topics: sets, union, intersection, difference, symmetric_difference

Set operations are essential for comparing datasets, finding overlaps,
and deduplicating records -- common tasks in data pipelines.

Tasks:
1. Find common elements between data sources
2. Find new/removed records between snapshots
3. Deduplicate records efficiently
"""

from typing import List, Set, Dict, Tuple, Any


def find_common_users(
    source_a: List[str],
    source_b: List[str]
) -> List[str]:
    """
    Find users that exist in both data sources.

    Args:
        source_a: List of user IDs from source A (may contain duplicates)
        source_b: List of user IDs from source B (may contain duplicates)

    Returns:
        Sorted list of user IDs found in both sources.
    """
    # TODO: Implement using set intersection
    pass


def find_changes(
    old_snapshot: List[str],
    new_snapshot: List[str]
) -> Dict[str, List[str]]:
    """
    Compare two snapshots to find what was added, removed, and unchanged.

    Args:
        old_snapshot: List of record IDs in the old snapshot
        new_snapshot: List of record IDs in the new snapshot

    Returns:
        Dictionary with three sorted lists:
        - 'added': IDs in new but not in old
        - 'removed': IDs in old but not in new
        - 'unchanged': IDs in both old and new
    """
    # TODO: Implement using set operations
    pass


def deduplicate_records(
    records: List[Dict[str, Any]],
    key_fields: List[str]
) -> List[Dict[str, Any]]:
    """
    Deduplicate records based on specified key fields.
    Keep the first occurrence of each unique key combination.

    Args:
        records: List of dictionaries representing records
        key_fields: List of field names that together form the unique key

    Returns:
        Deduplicated list of records, preserving original order.

    Example:
        records = [{'id': 1, 'name': 'A'}, {'id': 1, 'name': 'B'}, {'id': 2, 'name': 'C'}]
        deduplicate_records(records, ['id']) -> [{'id': 1, 'name': 'A'}, {'id': 2, 'name': 'C'}]
    """
    # TODO: Implement using a set to track seen keys
    pass


def symmetric_diff_analysis(
    dataset_a: List[str],
    dataset_b: List[str]
) -> Tuple[List[str], int, int, int]:
    """
    Perform symmetric difference analysis between two datasets.

    Args:
        dataset_a: First dataset of IDs
        dataset_b: Second dataset of IDs

    Returns:
        Tuple of:
        - Sorted list of IDs that are in exactly one of the datasets
        - Count of IDs only in A
        - Count of IDs only in B
        - Count of IDs in both (intersection size)
    """
    # TODO: Implement using set symmetric_difference and other operations
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_find_common_users():
    """Test finding common users."""
    result = find_common_users(
        ['user1', 'user2', 'user3', 'user2'],
        ['user2', 'user3', 'user4', 'user3']
    )
    assert result == ['user2', 'user3'], f"Expected ['user2', 'user3'], got {result}"

    result_empty = find_common_users(['a', 'b'], ['c', 'd'])
    assert result_empty == [], f"Expected empty list, got {result_empty}"

    print("PASS: Finding common users works correctly")


def test_find_changes():
    """Test snapshot comparison."""
    result = find_changes(
        ['rec1', 'rec2', 'rec3', 'rec4'],
        ['rec2', 'rec3', 'rec5', 'rec6']
    )

    assert result['added'] == ['rec5', 'rec6'], f"Added: {result['added']}"
    assert result['removed'] == ['rec1', 'rec4'], f"Removed: {result['removed']}"
    assert result['unchanged'] == ['rec2', 'rec3'], f"Unchanged: {result['unchanged']}"

    print("PASS: Snapshot comparison works correctly")


def test_deduplicate_records():
    """Test record deduplication."""
    records = [
        {'id': 1, 'name': 'Alice', 'score': 90},
        {'id': 2, 'name': 'Bob', 'score': 85},
        {'id': 1, 'name': 'Alice Updated', 'score': 95},
        {'id': 3, 'name': 'Charlie', 'score': 80},
        {'id': 2, 'name': 'Bob Again', 'score': 88}
    ]

    result = deduplicate_records(records, ['id'])
    assert len(result) == 3, f"Expected 3 unique records, got {len(result)}"
    assert result[0]['name'] == 'Alice', "Should keep first occurrence"
    assert result[1]['name'] == 'Bob', "Should keep first occurrence"

    # Multi-key dedup
    records_multi = [
        {'dept': 'eng', 'role': 'senior', 'name': 'A'},
        {'dept': 'eng', 'role': 'junior', 'name': 'B'},
        {'dept': 'eng', 'role': 'senior', 'name': 'C'},
    ]
    result_multi = deduplicate_records(records_multi, ['dept', 'role'])
    assert len(result_multi) == 2, f"Expected 2 unique dept+role combos, got {len(result_multi)}"

    print("PASS: Record deduplication works correctly")


def test_symmetric_diff():
    """Test symmetric difference analysis."""
    sym_diff, only_a, only_b, both = symmetric_diff_analysis(
        ['a', 'b', 'c', 'd'],
        ['c', 'd', 'e', 'f']
    )

    assert sym_diff == ['a', 'b', 'e', 'f'], f"Symmetric diff: {sym_diff}"
    assert only_a == 2, f"Only in A: {only_a}"
    assert only_b == 2, f"Only in B: {only_b}"
    assert both == 2, f"In both: {both}"

    print("PASS: Symmetric difference analysis works correctly")


if __name__ == "__main__":
    test_find_common_users()
    test_find_changes()
    test_deduplicate_records()
    test_symmetric_diff()
    print("\nAll tests passed! Great job!")

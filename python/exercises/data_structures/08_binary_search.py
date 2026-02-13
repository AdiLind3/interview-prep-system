# -*- coding: utf-8 -*-
"""
Problem: Binary search patterns for efficient data lookups

Difficulty: Medium
Estimated Time: 20 minutes
Topics: binary search, bisect, sorted data, boundary finding

Binary search is O(log n) vs O(n) for linear search -- critical for
large datasets. These patterns appear in database indexing, data
partitioning, and efficient lookups.

Tasks:
1. Classic binary search
2. Find insertion point (lower/upper bounds)
3. Search in a rotated sorted array
4. Find the closest value
"""

from typing import List, Optional, Tuple


def binary_search(arr: List[int], target: int) -> int:
    """
    Find the index of target in a sorted array.

    Args:
        arr: Sorted list of integers (ascending)
        target: Value to find

    Returns:
        Index of target if found, -1 otherwise.
    """
    # TODO: Implement classic binary search
    pass


def find_bounds(arr: List[int], target: int) -> Tuple[int, int]:
    """
    Find the first and last occurrence of target in a sorted array.

    Args:
        arr: Sorted list of integers (may contain duplicates)
        target: Value to find

    Returns:
        Tuple of (first_index, last_index).
        If target is not found, return (-1, -1).

    Example:
        arr = [1, 2, 2, 2, 3, 4], target = 2
        Returns: (1, 3)
    """
    # TODO: Implement using two binary searches (one for left bound, one for right)
    pass


def search_rotated(arr: List[int], target: int) -> int:
    """
    Search for target in a rotated sorted array.

    A rotated sorted array is a sorted array that has been rotated at some pivot.
    e.g., [4, 5, 6, 7, 0, 1, 2] is [0, 1, 2, 4, 5, 6, 7] rotated at index 4.

    Args:
        arr: Rotated sorted array of unique integers
        target: Value to find

    Returns:
        Index of target if found, -1 otherwise.

    Must run in O(log n) time.
    """
    # TODO: Implement modified binary search for rotated arrays
    pass


def find_closest(arr: List[int], target: int) -> int:
    """
    Find the value in the sorted array closest to target.

    Args:
        arr: Sorted list of integers (non-empty)
        target: Value to find the closest match for

    Returns:
        The value in arr closest to target.
        If two values are equally close, return the smaller one.
    """
    # TODO: Implement using binary search to find insertion point
    pass


def count_in_range(arr: List[int], low: int, high: int) -> int:
    """
    Count how many elements in the sorted array fall within [low, high] (inclusive).

    Args:
        arr: Sorted list of integers
        low: Lower bound (inclusive)
        high: Upper bound (inclusive)

    Returns:
        Count of elements where low <= element <= high.

    Must run in O(log n) time.
    """
    # TODO: Implement using binary search for both bounds
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_binary_search():
    """Test basic binary search."""
    arr = [1, 3, 5, 7, 9, 11, 13, 15]

    assert binary_search(arr, 7) == 3, f"Expected index 3 for target 7"
    assert binary_search(arr, 1) == 0, f"Expected index 0 for target 1"
    assert binary_search(arr, 15) == 7, f"Expected index 7 for target 15"
    assert binary_search(arr, 6) == -1, f"Expected -1 for missing target 6"
    assert binary_search([], 5) == -1, f"Expected -1 for empty array"

    print("PASS: Binary search works correctly")


def test_find_bounds():
    """Test finding first and last occurrence."""
    arr = [1, 2, 2, 2, 3, 4, 4, 5]

    assert find_bounds(arr, 2) == (1, 3), f"Bounds of 2: {find_bounds(arr, 2)}"
    assert find_bounds(arr, 4) == (5, 6), f"Bounds of 4: {find_bounds(arr, 4)}"
    assert find_bounds(arr, 1) == (0, 0), f"Bounds of 1: {find_bounds(arr, 1)}"
    assert find_bounds(arr, 6) == (-1, -1), f"Bounds of 6: {find_bounds(arr, 6)}"

    print("PASS: Finding bounds works correctly")


def test_search_rotated():
    """Test search in rotated sorted array."""
    arr = [4, 5, 6, 7, 0, 1, 2]

    assert search_rotated(arr, 0) == 4, f"Expected index 4 for target 0"
    assert search_rotated(arr, 4) == 0, f"Expected index 0 for target 4"
    assert search_rotated(arr, 7) == 3, f"Expected index 3 for target 7"
    assert search_rotated(arr, 3) == -1, f"Expected -1 for missing target 3"

    # Not rotated (edge case)
    assert search_rotated([1, 2, 3], 2) == 1, f"Non-rotated array should work"

    print("PASS: Rotated array search works correctly")


def test_find_closest():
    """Test finding closest value."""
    arr = [1, 4, 6, 8, 12, 15]

    assert find_closest(arr, 7) == 6, f"Closest to 7 should be 6, got {find_closest(arr, 7)}"
    assert find_closest(arr, 5) == 4, f"Closest to 5 should be 4 (tie, pick smaller), got {find_closest(arr, 5)}"
    assert find_closest(arr, 1) == 1, f"Exact match should return 1"
    assert find_closest(arr, 20) == 15, f"Beyond range should return 15"
    assert find_closest(arr, 0) == 1, f"Below range should return 1"

    print("PASS: Finding closest value works correctly")


def test_count_in_range():
    """Test counting elements in range."""
    arr = [1, 3, 5, 7, 9, 11, 13, 15]

    assert count_in_range(arr, 5, 11) == 4, f"Expected 4 elements in [5, 11]"
    assert count_in_range(arr, 1, 15) == 8, f"Expected 8 elements in [1, 15]"
    assert count_in_range(arr, 6, 8) == 1, f"Expected 1 element in [6, 8]"
    assert count_in_range(arr, 20, 30) == 0, f"Expected 0 elements in [20, 30]"
    assert count_in_range(arr, 2, 4) == 1, f"Expected 1 element in [2, 4]"

    print("PASS: Range counting works correctly")


if __name__ == "__main__":
    test_binary_search()
    test_find_bounds()
    test_search_rotated()
    test_find_closest()
    test_count_in_range()
    print("\nAll tests passed! Great job!")

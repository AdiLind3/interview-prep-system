# -*- coding: utf-8 -*-
"""
Problem: Master list comprehensions for data transformation

Difficulty: Easy
Estimated Time: 10 minutes
Topics: list comprehensions, nested comprehensions, filtering, flattening

List comprehensions are the Pythonic way to transform data.
These patterns appear constantly in data engineering code.

Tasks:
1. Flatten a list of lists
2. Conditional filtering with comprehensions
3. Nested comprehension for matrix operations
"""

from typing import List, Tuple, Any


def flatten_list(nested: List[List[Any]]) -> List[Any]:
    """
    Flatten a list of lists into a single list using a list comprehension.

    Args:
        nested: A list of lists, e.g., [[1, 2], [3, 4], [5]]

    Returns:
        A flat list, e.g., [1, 2, 3, 4, 5]
    """
    # TODO: Implement using a single list comprehension
    pass


def filter_and_transform(
    records: List[dict],
    min_value: float,
    key: str
) -> List[float]:
    """
    Filter records where key >= min_value and return the values, doubled.

    Args:
        records: List of dictionaries, each containing the specified key
        min_value: Minimum value threshold (inclusive)
        key: Dictionary key to filter and extract

    Returns:
        List of values (doubled) for records meeting the threshold.

    Example:
        records = [{'score': 80}, {'score': 50}, {'score': 90}]
        filter_and_transform(records, 60, 'score') -> [160, 180]
    """
    # TODO: Implement using a list comprehension
    pass


def matrix_transpose(matrix: List[List[int]]) -> List[List[int]]:
    """
    Transpose a matrix (list of lists) using a nested list comprehension.

    Args:
        matrix: 2D list where all inner lists have the same length.
                e.g., [[1, 2, 3], [4, 5, 6]]

    Returns:
        Transposed matrix. e.g., [[1, 4], [2, 5], [3, 6]]
    """
    # TODO: Implement using a nested list comprehension
    pass


def generate_pairs(
    list_a: List[Any],
    list_b: List[Any],
    exclude_equal: bool = True
) -> List[Tuple[Any, Any]]:
    """
    Generate all pairs (a, b) from two lists.

    Args:
        list_a: First list
        list_b: Second list
        exclude_equal: If True, exclude pairs where a == b

    Returns:
        List of tuples (a, b) for all combinations.
    """
    # TODO: Implement using a list comprehension with conditional
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_flatten_list():
    """Test list flattening."""
    assert flatten_list([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
    assert flatten_list([[], [1], []]) == [1]
    assert flatten_list([]) == []
    assert flatten_list([['a', 'b'], ['c']]) == ['a', 'b', 'c']

    print("PASS: List flattening works correctly")


def test_filter_and_transform():
    """Test filtering and transformation."""
    records = [
        {'score': 80, 'name': 'Alice'},
        {'score': 50, 'name': 'Bob'},
        {'score': 90, 'name': 'Charlie'},
        {'score': 60, 'name': 'Diana'}
    ]

    result = filter_and_transform(records, 60, 'score')
    assert result == [160, 100, 180, 120], f"Expected [160, 100, 180, 120], got {result}"

    result_high = filter_and_transform(records, 85, 'score')
    assert result_high == [180], f"Expected [180], got {result_high}"

    print("PASS: Filter and transform works correctly")


def test_matrix_transpose():
    """Test matrix transposition."""
    matrix = [[1, 2, 3], [4, 5, 6]]
    result = matrix_transpose(matrix)
    assert result == [[1, 4], [2, 5], [3, 6]], f"Expected [[1, 4], [2, 5], [3, 6]], got {result}"

    single_row = [[1, 2, 3]]
    assert matrix_transpose(single_row) == [[1], [2], [3]]

    print("PASS: Matrix transpose works correctly")


def test_generate_pairs():
    """Test pair generation."""
    result = generate_pairs([1, 2], ['a', 'b'])
    assert result == [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')], f"Got {result}"

    result_exclude = generate_pairs([1, 2, 3], [2, 3, 4], exclude_equal=True)
    assert (2, 2) not in result_exclude, "Equal pairs should be excluded"
    assert (3, 3) not in result_exclude, "Equal pairs should be excluded"
    assert (1, 2) in result_exclude, "Non-equal pairs should be included"

    result_include = generate_pairs([1, 2], [1, 2], exclude_equal=False)
    assert (1, 1) in result_include, "Equal pairs should be included when exclude_equal=False"

    print("PASS: Pair generation works correctly")


if __name__ == "__main__":
    test_flatten_list()
    test_filter_and_transform()
    test_matrix_transpose()
    test_generate_pairs()
    print("\nAll tests passed! Great job!")

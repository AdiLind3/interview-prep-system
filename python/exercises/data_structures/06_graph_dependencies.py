# -*- coding: utf-8 -*-
"""
Problem: Implement topological sort for pipeline dependency resolution

Difficulty: Hard
Estimated Time: 25 minutes
Topics: graphs, topological sort, DAGs, cycle detection, Airflow DAGs

In data engineering, tasks often depend on each other (like Airflow DAGs).
Topological sorting determines the correct execution order.

Tasks:
1. Build an adjacency list from dependency definitions
2. Detect cycles (invalid DAGs)
3. Perform topological sort (Kahn's algorithm)
4. Find all possible execution orders (parallel stages)
"""

import logging
from typing import List, Dict, Set, Optional, Tuple
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def build_graph(
    dependencies: Dict[str, List[str]]
) -> Tuple[Dict[str, Set[str]], Dict[str, int]]:
    """
    Build an adjacency list and in-degree map from dependency definitions.

    Args:
        dependencies: Dict mapping task_name -> list of tasks it depends on.
                      e.g., {'build': ['lint'], 'test': ['build']}
                      means 'build' depends on 'lint', 'test' depends on 'build'.

    Returns:
        Tuple of:
        - adjacency: Dict mapping each node to the set of nodes it points TO.
          (if A depends on B, then B -> A in the adjacency list)
        - in_degree: Dict mapping each node to its in-degree count.
          All nodes from dependencies (both keys and values) must be included.
    """
    # TODO: Implement your solution here
    pass


def detect_cycle(
    adjacency: Dict[str, Set[str]],
    in_degree: Dict[str, int]
) -> bool:
    """
    Detect if the dependency graph contains a cycle.

    A cycle means the tasks cannot be completed (circular dependency).

    Args:
        adjacency: Adjacency list (node -> set of nodes it points to)
        in_degree: In-degree map (node -> count of incoming edges)

    Returns:
        True if a cycle exists, False if the graph is a valid DAG.

    Hint: Use Kahn's algorithm -- if you cannot process all nodes, there is a cycle.
    """
    # TODO: Implement your solution here
    pass


def topological_sort(
    dependencies: Dict[str, List[str]]
) -> Optional[List[str]]:
    """
    Perform topological sort on task dependencies.

    Args:
        dependencies: Dict mapping task_name -> list of tasks it depends on.

    Returns:
        List of task names in valid execution order (dependencies before dependents).
        Returns None if the graph has a cycle.
        When multiple valid orderings exist, prefer alphabetical order.
    """
    # TODO: Implement using Kahn's algorithm
    # Use a sorted structure (like a heap or sorted list) instead of a plain queue
    # to ensure alphabetical ordering when multiple nodes have in-degree 0.
    pass


def find_parallel_stages(
    dependencies: Dict[str, List[str]]
) -> Optional[List[List[str]]]:
    """
    Group tasks into parallel execution stages.

    Each stage contains tasks that can run in parallel (all dependencies satisfied).
    Tasks within each stage are sorted alphabetically.

    Args:
        dependencies: Dict mapping task_name -> list of tasks it depends on.

    Returns:
        List of stages, where each stage is a sorted list of task names.
        Returns None if the graph has a cycle.

    Example:
        dependencies = {'A': [], 'B': ['A'], 'C': ['A'], 'D': ['B', 'C']}
        Returns: [['A'], ['B', 'C'], ['D']]
        Stage 1: A (no deps), Stage 2: B and C (only depend on A), Stage 3: D
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_build_graph():
    """Test graph construction."""
    deps = {
        'build': ['lint'],
        'test': ['build'],
        'deploy': ['test', 'build'],
        'lint': []
    }

    adjacency, in_degree = build_graph(deps)

    # lint -> build (lint has outgoing edge to build)
    assert 'build' in adjacency.get('lint', set()), "lint should point to build"
    assert 'test' in adjacency.get('build', set()), "build should point to test"

    assert in_degree['lint'] == 0, f"lint in-degree should be 0, got {in_degree['lint']}"
    assert in_degree['build'] == 1, f"build in-degree should be 1, got {in_degree['build']}"
    assert in_degree['deploy'] == 2, f"deploy in-degree should be 2, got {in_degree['deploy']}"

    print("PASS: Graph construction works correctly")


def test_detect_cycle():
    """Test cycle detection."""
    # No cycle
    deps_ok = {'A': [], 'B': ['A'], 'C': ['B']}
    adj, indeg = build_graph(deps_ok)
    assert not detect_cycle(adj, indeg), "Linear chain should not have a cycle"

    # Has cycle: A -> B -> C -> A
    deps_cycle = {'A': ['C'], 'B': ['A'], 'C': ['B']}
    adj2, indeg2 = build_graph(deps_cycle)
    assert detect_cycle(adj2, indeg2), "Circular dependency should be detected"

    print("PASS: Cycle detection works correctly")


def test_topological_sort():
    """Test topological sorting."""
    deps = {
        'deploy': ['test', 'build'],
        'test': ['build'],
        'build': ['lint'],
        'lint': []
    }

    result = topological_sort(deps)
    assert result is not None, "Should return a valid ordering"
    assert result == ['lint', 'build', 'test', 'deploy'], f"Expected ['lint', 'build', 'test', 'deploy'], got {result}"

    # Test with cycle
    deps_cycle = {'A': ['B'], 'B': ['C'], 'C': ['A']}
    result_cycle = topological_sort(deps_cycle)
    assert result_cycle is None, "Should return None for cyclic graph"

    print("PASS: Topological sort works correctly")


def test_topological_sort_alphabetical():
    """Test that topological sort prefers alphabetical order."""
    deps = {
        'C': [],
        'B': [],
        'A': [],
        'D': ['A', 'B', 'C']
    }

    result = topological_sort(deps)
    assert result is not None, "Should return a valid ordering"
    # A, B, C should come before D, and in alphabetical order
    assert result[-1] == 'D', f"D should be last, got {result}"
    assert result[:3] == ['A', 'B', 'C'], f"A, B, C should be first in alpha order, got {result}"

    print("PASS: Alphabetical topological sort works correctly")


def test_find_parallel_stages():
    """Test parallel stage grouping."""
    deps = {
        'extract_a': [],
        'extract_b': [],
        'transform_a': ['extract_a'],
        'transform_b': ['extract_b'],
        'merge': ['transform_a', 'transform_b'],
        'load': ['merge']
    }

    result = find_parallel_stages(deps)
    assert result is not None, "Should return stages for valid DAG"
    assert len(result) == 4, f"Expected 4 stages, got {len(result)}"

    assert result[0] == ['extract_a', 'extract_b'], f"Stage 1: {result[0]}"
    assert result[1] == ['transform_a', 'transform_b'], f"Stage 2: {result[1]}"
    assert result[2] == ['merge'], f"Stage 3: {result[2]}"
    assert result[3] == ['load'], f"Stage 4: {result[3]}"

    print("PASS: Parallel stage grouping works correctly")


if __name__ == "__main__":
    test_build_graph()
    test_detect_cycle()
    test_topological_sort()
    test_topological_sort_alphabetical()
    test_find_parallel_stages()
    print("\nAll tests passed! Great job!")

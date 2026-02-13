# -*- coding: utf-8 -*-
"""
Problem: Implement task queue and stack patterns for job processing

Difficulty: Medium
Estimated Time: 15 minutes
Topics: deque, queue, stack, FIFO, LIFO, job processing

Queues and stacks are fundamental for:
- Job processing systems (like Celery, SQS)
- Undo/redo functionality
- BFS/DFS algorithms
- Rate-limited API calls

Tasks:
1. Implement a bounded task queue with priority
2. Implement a stack-based expression evaluator
3. Simulate batch job processing with a deque
"""

import logging
from typing import Any, List, Optional, Tuple
from collections import deque
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass(order=True)
class Task:
    """A task with priority (lower number = higher priority)."""
    priority: int
    name: str = field(compare=False)
    payload: Any = field(compare=False, default=None)


class BoundedTaskQueue:
    """
    A bounded task queue that processes tasks in priority order.
    When the queue is full, new tasks are rejected.
    """

    def __init__(self, max_size: int):
        """
        Initialize the queue.

        Args:
            max_size: Maximum number of tasks the queue can hold.
        """
        # TODO: Initialize your data structures
        self.max_size = max_size

    def enqueue(self, task: Task) -> bool:
        """
        Add a task to the queue.

        Args:
            task: Task to add.

        Returns:
            True if task was added, False if queue is full.
        """
        # TODO: Implement your solution here
        pass

    def dequeue(self) -> Optional[Task]:
        """
        Remove and return the highest priority task (lowest priority number).

        Returns:
            The highest priority Task, or None if queue is empty.
        """
        # TODO: Implement your solution here
        pass

    def peek(self) -> Optional[Task]:
        """
        Return the highest priority task without removing it.

        Returns:
            The highest priority Task, or None if queue is empty.
        """
        # TODO: Implement your solution here
        pass

    def size(self) -> int:
        """Return the current number of tasks in the queue."""
        # TODO: Implement your solution here
        pass

    def is_empty(self) -> bool:
        """Return True if the queue is empty."""
        # TODO: Implement your solution here
        pass


def evaluate_rpn(expression: List[str]) -> float:
    """
    Evaluate a Reverse Polish Notation (RPN) expression using a stack.

    RPN (postfix notation) is used in many calculation engines.
    Operators come after their operands: "3 4 +" means 3 + 4.

    Args:
        expression: List of tokens. Numbers as strings, operators: +, -, *, /

    Returns:
        Result of the expression as a float.

    Example:
        ["3", "4", "+", "2", "*"] -> (3 + 4) * 2 = 14.0
        ["5", "1", "2", "+", "4", "*", "+", "3", "-"] -> 5 + (1+2)*4 - 3 = 14.0
    """
    # TODO: Implement using a stack (list)
    pass


def process_batch_jobs(
    jobs: List[str],
    batch_size: int,
    max_retries: int = 2
) -> Tuple[List[str], List[str]]:
    """
    Process jobs in batches using a deque. Failed jobs are retried.

    Simulate job processing where:
    - Jobs containing 'fail' will fail on first attempt but succeed on retry
    - Jobs containing 'error' will always fail
    - All other jobs succeed immediately

    Args:
        jobs: List of job names to process
        batch_size: Number of jobs to process in each batch
        max_retries: Maximum retry attempts for failed jobs

    Returns:
        Tuple of:
        - List of successfully processed job names (in order of completion)
        - List of permanently failed job names (in order of final failure)
    """
    # TODO: Implement using deque for the job queue
    # Hint: Use a deque, process batch_size items at a time
    # Track retry counts per job
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_bounded_task_queue():
    """Test the bounded task queue."""
    queue = BoundedTaskQueue(max_size=3)

    assert queue.is_empty(), "New queue should be empty"
    assert queue.size() == 0, "New queue size should be 0"

    # Add tasks
    assert queue.enqueue(Task(priority=3, name='low_task')), "Should accept task"
    assert queue.enqueue(Task(priority=1, name='high_task')), "Should accept task"
    assert queue.enqueue(Task(priority=2, name='mid_task')), "Should accept task"
    assert not queue.enqueue(Task(priority=0, name='overflow_task')), "Should reject (queue full)"

    assert queue.size() == 3, f"Queue size should be 3, got {queue.size()}"

    # Peek should return highest priority (lowest number)
    peeked = queue.peek()
    assert peeked is not None and peeked.name == 'high_task', f"Peek should return high_task, got {peeked}"

    # Dequeue in priority order
    task1 = queue.dequeue()
    assert task1 is not None and task1.name == 'high_task', f"First dequeue: {task1}"

    task2 = queue.dequeue()
    assert task2 is not None and task2.name == 'mid_task', f"Second dequeue: {task2}"

    task3 = queue.dequeue()
    assert task3 is not None and task3.name == 'low_task', f"Third dequeue: {task3}"

    assert queue.dequeue() is None, "Dequeue from empty queue should return None"

    print("PASS: Bounded task queue works correctly")


def test_evaluate_rpn():
    """Test RPN expression evaluation."""
    # 3 + 4 = 7
    assert evaluate_rpn(["3", "4", "+"]) == 7.0, "3 4 + should be 7"

    # (3 + 4) * 2 = 14
    assert evaluate_rpn(["3", "4", "+", "2", "*"]) == 14.0, "3 4 + 2 * should be 14"

    # 5 + ((1 + 2) * 4) - 3 = 14
    result = evaluate_rpn(["5", "1", "2", "+", "4", "*", "+", "3", "-"])
    assert result == 14.0, f"Expected 14.0, got {result}"

    # 10 / 3 (float division)
    result_div = evaluate_rpn(["10", "3", "/"])
    assert abs(result_div - 10 / 3) < 0.001, f"10 / 3 should be ~3.333, got {result_div}"

    print("PASS: RPN evaluation works correctly")


def test_process_batch_jobs():
    """Test batch job processing."""
    jobs = ['job_a', 'job_fail_b', 'job_c', 'job_error_d', 'job_e']

    succeeded, failed = process_batch_jobs(jobs, batch_size=2, max_retries=2)

    # job_a, job_c, job_e should succeed immediately
    # job_fail_b should fail first then succeed on retry
    # job_error_d should always fail
    assert 'job_a' in succeeded, "job_a should succeed"
    assert 'job_c' in succeeded, "job_c should succeed"
    assert 'job_e' in succeeded, "job_e should succeed"
    assert 'job_fail_b' in succeeded, "job_fail_b should succeed after retry"
    assert 'job_error_d' in failed, "job_error_d should permanently fail"

    print("PASS: Batch job processing works correctly")


if __name__ == "__main__":
    test_bounded_task_queue()
    test_evaluate_rpn()
    test_process_batch_jobs()
    print("\nAll tests passed! Great job!")

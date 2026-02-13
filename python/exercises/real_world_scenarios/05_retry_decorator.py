# -*- coding: utf-8 -*-
"""
Problem: Build a retry decorator with exponential backoff

Difficulty: Medium
Estimated Time: 15 minutes
Topics: decorators, exponential backoff, error handling, design patterns

Retry logic with exponential backoff is one of the most common patterns
in data engineering. Used in: API calls, database connections, cloud
service interactions, message queue publishing, etc.

Tasks:
1. Build a basic retry decorator
2. Add exponential backoff with jitter
3. Support selective exception handling
"""

import logging
import time
import random
import functools
from typing import Any, Callable, Optional, Tuple, Type, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def retry(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception, float], None]] = None
) -> Callable:
    """
    A decorator that retries a function on failure with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (not counting the first call).
        backoff_factor: Multiplier for delay between retries.
                        delay = initial_delay * (backoff_factor ** attempt)
        initial_delay: Starting delay in seconds before the first retry.
        max_delay: Maximum delay in seconds (cap).
        retryable_exceptions: Tuple of exception types that trigger a retry.
                              Other exceptions are raised immediately.
        on_retry: Optional callback called before each retry with
                  (attempt_number, exception, delay_seconds).

    Returns:
        Decorated function that retries on failure.

    Behavior:
        - First call is attempt 0 (not counted as a retry)
        - If it fails with a retryable exception, retry up to max_retries times
        - Delay before retry i (1-indexed) = min(initial_delay * backoff_factor^(i-1), max_delay)
        - If on_retry callback is provided, call it before sleeping
        - If all retries are exhausted, raise the last exception
        - If a non-retryable exception occurs, raise it immediately

    NOTE: For testing purposes, do NOT actually call time.sleep.
    Instead, just calculate the delay and call on_retry if provided.
    This makes tests fast and deterministic.
    """
    # TODO: Implement the decorator
    # Hint: This is a three-level nested function:
    # retry(args) -> decorator(func) -> wrapper(*args, **kwargs)
    pass


def retry_with_result(
    max_retries: int = 3,
    retry_on_result: Optional[Callable[[Any], bool]] = None,
    backoff_factor: float = 2.0,
    initial_delay: float = 1.0
) -> Callable:
    """
    A decorator that retries based on the return value (not just exceptions).

    Sometimes a function returns a "bad" result instead of raising an exception
    (e.g., an API returns {'status': 'error'} instead of raising).

    Args:
        max_retries: Maximum retry attempts
        retry_on_result: A callable that takes the function result and returns
                         True if the result is "bad" and should be retried.
                         If None, only retry on exceptions.
        backoff_factor: Multiplier for delay between retries.
        initial_delay: Starting delay in seconds.

    Returns:
        Decorated function.

    NOTE: For testing purposes, do NOT actually call time.sleep.
    """
    # TODO: Implement the decorator
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_basic_retry():
    """Test basic retry on exception."""
    call_count = 0

    @retry(max_retries=3, initial_delay=0.01, backoff_factor=2.0)
    def flaky_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Connection failed")
        return "success"

    result = flaky_function()
    assert result == "success", f"Expected 'success', got {result}"
    assert call_count == 3, f"Expected 3 calls, got {call_count}"

    print("PASS: Basic retry works correctly")


def test_max_retries_exceeded():
    """Test that exception is raised after max retries."""
    call_count = 0

    @retry(max_retries=2, initial_delay=0.01)
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise ValueError("Always fails")

    try:
        always_fails()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # 1 initial + 2 retries = 3
    assert call_count == 3, f"Expected 3 calls (1 + 2 retries), got {call_count}"

    print("PASS: Max retries exceeded raises exception")


def test_non_retryable_exception():
    """Test that non-retryable exceptions are raised immediately."""
    call_count = 0

    @retry(max_retries=3, initial_delay=0.01, retryable_exceptions=(ConnectionError,))
    def raises_type_error():
        nonlocal call_count
        call_count += 1
        raise TypeError("Not retryable")

    try:
        raises_type_error()
        assert False, "Should have raised TypeError"
    except TypeError:
        pass

    assert call_count == 1, f"Expected 1 call (no retry), got {call_count}"

    print("PASS: Non-retryable exceptions raised immediately")


def test_on_retry_callback():
    """Test on_retry callback."""
    retry_log = []

    def log_retry(attempt, exception, delay):
        retry_log.append({'attempt': attempt, 'error': str(exception), 'delay': delay})

    call_count = 0

    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, on_retry=log_retry)
    def fails_twice():
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            raise ConnectionError(f"Fail #{call_count}")
        return "done"

    result = fails_twice()
    assert result == "done", f"Expected 'done', got {result}"
    assert len(retry_log) == 2, f"Expected 2 retry logs, got {len(retry_log)}"

    # First retry: delay = 1.0 * 2^0 = 1.0
    assert retry_log[0]['delay'] == 1.0, f"First retry delay should be 1.0, got {retry_log[0]['delay']}"
    # Second retry: delay = 1.0 * 2^1 = 2.0
    assert retry_log[1]['delay'] == 2.0, f"Second retry delay should be 2.0, got {retry_log[1]['delay']}"

    print("PASS: On retry callback works correctly")


def test_retry_with_result_check():
    """Test retry based on return value."""
    call_count = 0

    @retry_with_result(
        max_retries=3,
        retry_on_result=lambda r: r.get('status') == 'error',
        initial_delay=0.01
    )
    def returns_error_then_ok():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return {'status': 'error', 'message': 'try again'}
        return {'status': 'ok', 'data': [1, 2, 3]}

    result = returns_error_then_ok()
    assert result['status'] == 'ok', f"Expected 'ok', got {result['status']}"
    assert call_count == 3, f"Expected 3 calls, got {call_count}"

    print("PASS: Retry with result check works correctly")


def test_no_retry_needed():
    """Test function that succeeds on first try."""
    call_count = 0

    @retry(max_retries=3, initial_delay=0.01)
    def always_works():
        nonlocal call_count
        call_count += 1
        return 42

    result = always_works()
    assert result == 42, f"Expected 42, got {result}"
    assert call_count == 1, f"Expected 1 call (no retries), got {call_count}"

    print("PASS: No retry when function succeeds")


if __name__ == "__main__":
    test_basic_retry()
    test_max_retries_exceeded()
    test_non_retryable_exception()
    test_on_retry_callback()
    test_retry_with_result_check()
    test_no_retry_needed()
    print("\nAll tests passed! Great job!")

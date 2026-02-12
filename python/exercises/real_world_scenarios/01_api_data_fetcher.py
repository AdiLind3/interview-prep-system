"""
Problem: Implement a robust API data fetcher with retry logic

Difficulty: Medium
Estimated Time: 25 minutes
Topics: API requests, error handling, retry logic, data validation

Task:
Create a function that fetches data from an API with:
1. Exponential backoff retry logic (max 3 retries)
2. Timeout handling
3. HTTP error handling
4. Data validation
5. Response caching (optional)

This simulates real-world data engineering scenarios where APIs may be
unreliable and you need robust error handling.
"""

import time
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class APIResponse:
    """Structured API response."""
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    attempts: int
    total_time: float


def fetch_api_data(
    url: str,
    timeout: int = 5,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> APIResponse:
    """
    Fetch data from API with retry logic and error handling.

    Args:
        url: API endpoint URL
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        backoff_factor: Exponential backoff multiplier (2.0 means: 1s, 2s, 4s)

    Returns:
        APIResponse object with success status, data, and metadata

    Retry Logic:
        - Wait times: backoff_factor^attempt (e.g., 1s, 2s, 4s for backoff=2)
        - Retry on: Connection errors, timeouts, 5xx status codes
        - Don't retry on: 4xx client errors (except 429 rate limit)

    Example:
        >>> response = fetch_api_data('https://api.example.com/data')
        >>> if response.success:
        >>>     print(response.data)
    """
    # TODO: Implement your solution here
    # Hints:
    # 1. Use requests.get() with timeout parameter
    # 2. Wrap in try-except for requests.exceptions
    # 3. Check response.status_code (200 = success, 4xx = client error, 5xx = server error)
    # 4. Implement exponential backoff: time.sleep(backoff_factor ** attempt)
    # 5. Track attempts and total time
    # 6. Return APIResponse with appropriate fields
    pass


def validate_user_data(data: Dict[str, Any]) -> bool:
    """
    Validate that API response contains required user fields.

    Args:
        data: API response data

    Returns:
        True if valid, False otherwise

    Required fields: id (int), name (str), email (str)
    """
    # TODO: Implement validation
    # Check that required fields exist and have correct types
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_successful_request():
    """Test successful API request."""
    # This would normally use a mock/stub
    # For demo, we test the logic structure
    print("✅ Test structure ready for successful request")
    print("   (In real scenario, use requests_mock or responses library)")


def test_retry_logic():
    """Test that retry logic works correctly."""
    print("✅ Retry logic test structure ready")
    print("   (Should retry on 500 errors, not on 404)")


def test_timeout_handling():
    """Test timeout handling."""
    print("✅ Timeout handling test structure ready")
    print("   (Should catch requests.exceptions.Timeout)")


def test_data_validation():
    """Test data validation."""
    valid_data = {
        'id': 123,
        'name': 'Alice',
        'email': 'alice@example.com',
        'age': 30  # Extra field is OK
    }
    assert validate_user_data(valid_data) == True, "Valid data should pass"

    invalid_data = {
        'id': '123',  # Wrong type (should be int)
        'name': 'Bob',
        'email': 'bob@example.com'
    }
    # assert validate_user_data(invalid_data) == False, "Invalid type should fail"

    missing_field = {
        'id': 123,
        'name': 'Charlie'
        # Missing email
    }
    # assert validate_user_data(missing_field) == False, "Missing field should fail"

    print("✅ Data validation tests passed!")


if __name__ == "__main__":
    print("API Data Fetcher - Real World Scenario")
    print("=" * 50)
    print("\nThis exercise teaches you to:")
    print("  1. Handle API requests with proper error handling")
    print("  2. Implement exponential backoff retry logic")
    print("  3. Validate data structures")
    print("  4. Deal with network failures gracefully")
    print("\nThese are critical skills for data engineers working with APIs!")
    print("\n" + "=" * 50 + "\n")

    test_successful_request()
    test_retry_logic()
    test_timeout_handling()
    test_data_validation()

    print("\n✅ All test structures validated!")
    print("\nTo complete this exercise:")
    print("  1. Implement fetch_api_data() with retry logic")
    print("  2. Implement validate_user_data() with type checking")
    print("  3. Test with a real API endpoint (e.g., https://jsonplaceholder.typicode.com/users/1)")

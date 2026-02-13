# -*- coding: utf-8 -*-
"""
Problem: Build a web scraper with rate limiting, error handling, and data extraction

Difficulty: Hard
Estimated Time: 30 minutes
Topics: web scraping, rate limiting, HTML parsing, error handling, data extraction

Web scraping is a valuable data engineering skill, especially for companies
like tasq.ai that need to collect data from various web sources.

This exercise builds a scraper framework with:
1. Rate limiting to respect server limits
2. Robust error handling
3. HTML data extraction (simulated)
4. Result collection and deduplication

NOTE: This exercise uses simulated HTML responses so no network calls are needed.
"""

import logging
import time
import re
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ScrapedItem:
    """A single scraped data item."""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScrapeResult:
    """Result of a scraping session."""
    total_urls: int
    successful: int
    failed: int
    items: List[ScrapedItem] = field(default_factory=list)
    errors: List[Dict[str, str]] = field(default_factory=list)


class RateLimiter:
    """
    A rate limiter using the token bucket algorithm.

    Ensures that no more than max_requests are made within the time_window.
    """

    def __init__(self, max_requests: int, time_window: float):
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in the time window.
            time_window: Time window in seconds.
        """
        # TODO: Initialize your data structures
        # Hint: Track request timestamps using a deque
        self.max_requests = max_requests
        self.time_window = time_window

    def can_proceed(self, current_time: float) -> bool:
        """
        Check if a request can proceed at the given time.

        Args:
            current_time: Current timestamp (as float seconds).

        Returns:
            True if the request can proceed, False if rate limit would be exceeded.

        Behavior:
            - Remove all timestamps older than (current_time - time_window)
            - If remaining timestamps count < max_requests, return True
            - Otherwise return False
        """
        # TODO: Implement your solution here
        pass

    def record_request(self, current_time: float) -> None:
        """
        Record that a request was made at the given time.

        Args:
            current_time: Timestamp of the request.
        """
        # TODO: Implement your solution here
        pass

    def wait_time(self, current_time: float) -> float:
        """
        Calculate how long to wait before the next request can proceed.

        Args:
            current_time: Current timestamp.

        Returns:
            Number of seconds to wait. 0.0 if can proceed immediately.
        """
        # TODO: Implement your solution here
        pass


def extract_data_from_html(html: str, patterns: Dict[str, str]) -> Dict[str, Optional[str]]:
    """
    Extract data from HTML content using regex patterns.

    Args:
        html: Raw HTML string
        patterns: Dict mapping field_name -> regex pattern.
                  Each pattern should have one capture group.

    Returns:
        Dict mapping field_name -> extracted value (or None if not found).
        Extracted values should be stripped of leading/trailing whitespace.
    """
    # TODO: Implement your solution here
    pass


def deduplicate_items(items: List[ScrapedItem], key: str = 'url') -> List[ScrapedItem]:
    """
    Deduplicate scraped items based on a key field.

    Args:
        items: List of ScrapedItem objects
        key: Attribute name to use as the dedup key ('url' or 'title')

    Returns:
        Deduplicated list, keeping the first occurrence of each key.
    """
    # TODO: Implement your solution here
    pass


def run_scraper(
    urls: List[str],
    fetch_fn: Callable[[str], Tuple[bool, str]],
    extract_patterns: Dict[str, str],
    rate_limiter: Optional[RateLimiter] = None
) -> ScrapeResult:
    """
    Run the scraper on a list of URLs.

    Args:
        urls: List of URLs to scrape
        fetch_fn: A function that takes a URL and returns (success: bool, html_or_error: str).
                  If success is True, html_or_error is the HTML content.
                  If success is False, html_or_error is an error message.
        extract_patterns: Regex patterns for data extraction
        rate_limiter: Optional RateLimiter instance.
                      For this exercise, if rate limiter says cannot proceed, skip the URL
                      and add it to errors with message 'Rate limited'.

    Returns:
        ScrapeResult with all scraped items and error details.
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_rate_limiter():
    """Test rate limiter."""
    limiter = RateLimiter(max_requests=3, time_window=10.0)

    # First 3 requests should be allowed
    assert limiter.can_proceed(1.0), "First request should be allowed"
    limiter.record_request(1.0)

    assert limiter.can_proceed(2.0), "Second request should be allowed"
    limiter.record_request(2.0)

    assert limiter.can_proceed(3.0), "Third request should be allowed"
    limiter.record_request(3.0)

    # Fourth request within window should be denied
    assert not limiter.can_proceed(4.0), "Fourth request should be denied"

    # After the window expires for the first request, should be allowed again
    assert limiter.can_proceed(12.0), "Should be allowed after window expires"

    # Test wait_time
    wait = limiter.wait_time(4.0)
    assert wait > 0, f"Should need to wait, got {wait}"

    print("PASS: Rate limiter works correctly")


def test_extract_data():
    """Test HTML data extraction."""
    html = """
    <html>
    <head><title>Test Page - Data Engineering</title></head>
    <body>
        <h1 class="main-title">Welcome to Data Engineering</h1>
        <p class="description">Learn about ETL pipelines and data processing.</p>
        <span class="author">By Alice Smith</span>
        <div class="date">Published: 2024-01-15</div>
    </body>
    </html>
    """

    patterns = {
        'title': r'<title>(.*?)</title>',
        'heading': r'<h1[^>]*>(.*?)</h1>',
        'description': r'<p class="description">(.*?)</p>',
        'author': r'<span class="author">(.*?)</span>',
        'missing_field': r'<div class="nonexistent">(.*?)</div>'
    }

    result = extract_data_from_html(html, patterns)

    assert result['title'] == 'Test Page - Data Engineering', f"Title: {result['title']}"
    assert result['heading'] == 'Welcome to Data Engineering', f"Heading: {result['heading']}"
    assert result['author'] == 'By Alice Smith', f"Author: {result['author']}"
    assert result['missing_field'] is None, "Missing field should be None"

    print("PASS: HTML data extraction works correctly")


def test_deduplicate_items():
    """Test item deduplication."""
    items = [
        ScrapedItem(url='http://a.com', title='Page A', content='Content A'),
        ScrapedItem(url='http://b.com', title='Page B', content='Content B'),
        ScrapedItem(url='http://a.com', title='Page A Dupe', content='Content A v2'),
        ScrapedItem(url='http://c.com', title='Page C', content='Content C'),
    ]

    result = deduplicate_items(items, key='url')
    assert len(result) == 3, f"Expected 3 unique items, got {len(result)}"
    assert result[0].title == 'Page A', "Should keep first occurrence"

    print("PASS: Deduplication works correctly")


def test_run_scraper():
    """Test the full scraper."""
    def mock_fetch(url: str) -> Tuple[bool, str]:
        """Simulated fetch function."""
        if 'error' in url:
            return (False, 'Connection refused')
        return (True, f'<html><title>Page for {url}</title><p class="desc">Content of {url}</p></html>')

    urls = [
        'http://example.com/page1',
        'http://example.com/page2',
        'http://example.com/error',
        'http://example.com/page3',
    ]

    patterns = {
        'title': r'<title>(.*?)</title>',
        'description': r'<p class="desc">(.*?)</p>'
    }

    result = run_scraper(urls, mock_fetch, patterns)

    assert result.total_urls == 4, f"Total URLs: {result.total_urls}"
    assert result.successful == 3, f"Successful: {result.successful}"
    assert result.failed == 1, f"Failed: {result.failed}"
    assert len(result.items) == 3, f"Items: {len(result.items)}"
    assert len(result.errors) == 1, f"Errors: {len(result.errors)}"

    print("PASS: Full scraper works correctly")


def test_scraper_with_rate_limit():
    """Test scraper with rate limiting."""
    def mock_fetch(url: str) -> Tuple[bool, str]:
        return (True, f'<html><title>Page</title></html>')

    urls = [f'http://example.com/page{i}' for i in range(5)]
    patterns = {'title': r'<title>(.*?)</title>'}

    # Allow only 3 requests in a very large window
    limiter = RateLimiter(max_requests=3, time_window=1000.0)

    result = run_scraper(urls, mock_fetch, patterns, rate_limiter=limiter)

    assert result.successful == 3, f"Should only succeed 3 times, got {result.successful}"
    assert result.failed == 2, f"Should fail 2 times (rate limited), got {result.failed}"

    print("PASS: Scraper with rate limiting works correctly")


if __name__ == "__main__":
    test_rate_limiter()
    test_extract_data()
    test_deduplicate_items()
    test_run_scraper()
    test_scraper_with_rate_limit()
    print("\nAll tests passed! Great job!")

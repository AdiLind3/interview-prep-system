# -*- coding: utf-8 -*-
"""
Problem: Parse server logs, extract patterns, aggregate errors, and generate a report

Difficulty: Medium
Estimated Time: 25 minutes
Topics: regex, log parsing, aggregation, text processing

Log parsing is a foundational skill for data engineers. You need to extract
structured data from semi-structured text -- a pattern that applies to
server logs, application logs, audit trails, and more.

Tasks:
1. Parse log lines into structured records
2. Filter and aggregate by severity
3. Extract patterns (IP addresses, error codes)
4. Generate a summary report
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class LogEntry:
    """A parsed log entry."""
    timestamp: str
    level: str
    source: str
    message: str
    ip_address: Optional[str] = None
    status_code: Optional[int] = None


def parse_log_line(line: str) -> Optional[LogEntry]:
    """
    Parse a single log line into a LogEntry.

    Expected format:
        [YYYY-MM-DD HH:MM:SS] LEVEL source - message

    Examples:
        [2024-01-15 10:30:45] ERROR api-server - Connection refused from 192.168.1.100
        [2024-01-15 10:30:46] INFO web-server - GET /api/users 200
        [2024-01-15 10:30:47] WARNING db-server - Slow query detected (3.5s)

    Args:
        line: Raw log line string

    Returns:
        LogEntry if the line matches the expected format, None otherwise.
        Also extract:
        - ip_address: Any IPv4 address found in the message (or None)
        - status_code: Any 3-digit HTTP status code found in the message (or None)
    """
    # TODO: Implement using regex
    # Hint: Use a regex pattern like r'\[(.+?)\] (\w+) ([\w-]+) - (.+)'
    pass


def filter_by_level(entries: List[LogEntry], level: str) -> List[LogEntry]:
    """
    Filter log entries by severity level (case-insensitive).

    Args:
        entries: List of LogEntry objects
        level: Log level to filter for (e.g., 'ERROR', 'WARNING')

    Returns:
        List of LogEntry objects matching the specified level.
    """
    # TODO: Implement your solution here
    pass


def aggregate_by_source(entries: List[LogEntry]) -> Dict[str, Dict[str, int]]:
    """
    Aggregate log entries by source, counting occurrences per level.

    Args:
        entries: List of LogEntry objects

    Returns:
        Dict mapping source -> {level: count}.

    Example:
        {'api-server': {'ERROR': 5, 'WARNING': 3, 'INFO': 10},
         'db-server': {'ERROR': 2, 'INFO': 15}}
    """
    # TODO: Implement your solution here
    pass


def top_ip_addresses(entries: List[LogEntry], n: int = 5) -> List[Tuple[str, int]]:
    """
    Find the top N most frequent IP addresses in log entries.

    Args:
        entries: List of LogEntry objects
        n: Number of top IPs to return

    Returns:
        List of (ip_address, count) tuples, sorted by count descending.
        Only includes entries that have an IP address.
    """
    # TODO: Implement your solution here
    pass


def generate_log_report(entries: List[LogEntry]) -> Dict[str, Any]:
    """
    Generate a comprehensive log analysis report.

    Args:
        entries: List of LogEntry objects

    Returns:
        Dictionary with:
        - total_entries: Total number of log entries
        - level_counts: Dict mapping level -> count
        - error_rate: Percentage of entries that are ERROR level, rounded to 2 decimals
        - top_error_sources: List of (source, count) for sources with most errors,
                             sorted by count descending
        - top_ips: Top 5 most frequent IP addresses as (ip, count) tuples
        - status_code_counts: Dict mapping status_code -> count (for entries with status codes)
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

# Sample log data for testing
SAMPLE_LOGS = [
    "[2024-01-15 10:30:45] ERROR api-server - Connection refused from 192.168.1.100",
    "[2024-01-15 10:30:46] INFO web-server - GET /api/users 200",
    "[2024-01-15 10:30:47] WARNING db-server - Slow query detected (3.5s)",
    "[2024-01-15 10:30:48] ERROR api-server - Timeout connecting to 192.168.1.200",
    "[2024-01-15 10:30:49] INFO web-server - POST /api/data 201",
    "[2024-01-15 10:30:50] ERROR db-server - Deadlock from 10.0.0.50",
    "[2024-01-15 10:30:51] INFO web-server - GET /api/health 200",
    "[2024-01-15 10:30:52] WARNING api-server - Rate limit approaching from 192.168.1.100",
    "[2024-01-15 10:30:53] ERROR api-server - Internal server error 500",
    "[2024-01-15 10:30:54] INFO web-server - GET /api/status 200",
    "this is a malformed line that should be skipped",
    "[2024-01-15 10:30:55] ERROR web-server - Service unavailable 503 from 172.16.0.1",
]


def test_parse_log_line():
    """Test log line parsing."""
    entry = parse_log_line("[2024-01-15 10:30:45] ERROR api-server - Connection refused from 192.168.1.100")

    assert entry is not None, "Should parse valid log line"
    assert entry.timestamp == "2024-01-15 10:30:45", f"Timestamp: {entry.timestamp}"
    assert entry.level == "ERROR", f"Level: {entry.level}"
    assert entry.source == "api-server", f"Source: {entry.source}"
    assert entry.ip_address == "192.168.1.100", f"IP: {entry.ip_address}"

    # Test with status code
    entry2 = parse_log_line("[2024-01-15 10:30:46] INFO web-server - GET /api/users 200")
    assert entry2 is not None, "Should parse line with status code"
    assert entry2.status_code == 200, f"Status code: {entry2.status_code}"

    # Test malformed line
    entry3 = parse_log_line("this is not a valid log line")
    assert entry3 is None, "Should return None for malformed lines"

    print("PASS: Log line parsing works correctly")


def test_filter_by_level():
    """Test filtering by log level."""
    entries = [parse_log_line(line) for line in SAMPLE_LOGS]
    entries = [e for e in entries if e is not None]

    errors = filter_by_level(entries, 'ERROR')
    assert len(errors) == 5, f"Expected 5 ERROR entries, got {len(errors)}"

    infos = filter_by_level(entries, 'INFO')
    assert len(infos) == 4, f"Expected 4 INFO entries, got {len(infos)}"

    print("PASS: Level filtering works correctly")


def test_aggregate_by_source():
    """Test aggregation by source."""
    entries = [parse_log_line(line) for line in SAMPLE_LOGS]
    entries = [e for e in entries if e is not None]

    result = aggregate_by_source(entries)

    assert 'api-server' in result, "Should have api-server"
    assert result['api-server'].get('ERROR', 0) == 3, \
        f"api-server errors: {result['api-server'].get('ERROR', 0)}"
    assert result['web-server'].get('INFO', 0) == 4, \
        f"web-server infos: {result['web-server'].get('INFO', 0)}"

    print("PASS: Source aggregation works correctly")


def test_top_ip_addresses():
    """Test top IP address extraction."""
    entries = [parse_log_line(line) for line in SAMPLE_LOGS]
    entries = [e for e in entries if e is not None]

    result = top_ip_addresses(entries, n=3)

    assert len(result) > 0, "Should find at least one IP"
    # 192.168.1.100 appears twice
    assert result[0][0] == '192.168.1.100', f"Most common IP should be 192.168.1.100, got {result[0][0]}"
    assert result[0][1] == 2, f"Expected count 2, got {result[0][1]}"

    print("PASS: Top IP addresses works correctly")


def test_generate_report():
    """Test full report generation."""
    entries = [parse_log_line(line) for line in SAMPLE_LOGS]
    entries = [e for e in entries if e is not None]

    report = generate_log_report(entries)

    assert report['total_entries'] == 11, f"Total entries: {report['total_entries']}"
    assert report['level_counts']['ERROR'] == 5, f"Error count: {report['level_counts'].get('ERROR')}"
    assert report['error_rate'] > 0, f"Error rate should be > 0"
    assert len(report['top_error_sources']) > 0, "Should have error sources"
    assert 200 in report['status_code_counts'], "Should have status code 200"

    print("PASS: Report generation works correctly")


if __name__ == "__main__":
    test_parse_log_line()
    test_filter_by_level()
    test_aggregate_by_source()
    test_top_ip_addresses()
    test_generate_report()
    print("\nAll tests passed! Great job!")

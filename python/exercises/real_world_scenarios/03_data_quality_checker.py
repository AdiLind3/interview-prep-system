# -*- coding: utf-8 -*-
"""
Problem: Build a data quality checker for validating datasets

Difficulty: Medium
Estimated Time: 20 minutes
Topics: data validation, completeness, type checking, data quality

Data quality is critical in data engineering. Bad data leads to bad decisions.
This exercise builds a reusable data quality framework.

Tasks:
1. Check completeness (null/missing values)
2. Check uniqueness constraints
3. Check type conformity
4. Generate a quality report
"""

import logging
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class QualityCheck:
    """A single quality check result."""
    check_name: str
    passed: bool
    details: str
    affected_count: int = 0


@dataclass
class QualityReport:
    """Complete quality report for a dataset."""
    total_records: int
    checks: List[QualityCheck] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """True if all checks passed."""
        return all(c.passed for c in self.checks)

    @property
    def summary(self) -> Dict[str, Any]:
        """Summary of the report."""
        return {
            'total_records': self.total_records,
            'total_checks': len(self.checks),
            'passed_checks': sum(1 for c in self.checks if c.passed),
            'failed_checks': sum(1 for c in self.checks if not c.passed),
            'overall_passed': self.passed
        }


def check_completeness(
    records: List[Dict[str, Any]],
    required_fields: List[str]
) -> QualityCheck:
    """
    Check that required fields are not null/None/empty-string in any record.

    Args:
        records: List of record dictionaries
        required_fields: Fields that must have non-null, non-empty values

    Returns:
        QualityCheck with:
        - check_name: 'completeness'
        - passed: True if all required fields have values in all records
        - details: Description of what was found
        - affected_count: Number of records with at least one missing required field
    """
    # TODO: Implement your solution here
    pass


def check_uniqueness(
    records: List[Dict[str, Any]],
    unique_fields: List[str]
) -> QualityCheck:
    """
    Check that the combination of specified fields is unique across all records.

    Args:
        records: List of record dictionaries
        unique_fields: Fields that together should form a unique key

    Returns:
        QualityCheck with:
        - check_name: 'uniqueness'
        - passed: True if no duplicate key combinations found
        - details: Description of duplicates found (if any)
        - affected_count: Number of duplicate records (total records - unique records)
    """
    # TODO: Implement your solution here
    pass


def check_type_conformity(
    records: List[Dict[str, Any]],
    type_specs: Dict[str, type]
) -> QualityCheck:
    """
    Check that field values match expected types.

    Args:
        records: List of record dictionaries
        type_specs: Dict mapping field_name -> expected Python type.
                    e.g., {'age': int, 'name': str, 'salary': float}
                    None values are allowed and should not cause failure.

    Returns:
        QualityCheck with:
        - check_name: 'type_conformity'
        - passed: True if all non-null values match expected types
        - details: Description of type mismatches
        - affected_count: Number of records with at least one type mismatch
    """
    # TODO: Implement your solution here
    pass


def check_value_ranges(
    records: List[Dict[str, Any]],
    range_specs: Dict[str, Dict[str, Any]]
) -> QualityCheck:
    """
    Check that numeric field values fall within specified ranges.

    Args:
        records: List of record dictionaries
        range_specs: Dict mapping field_name -> {'min': value, 'max': value}.
                     Either 'min' or 'max' can be omitted for one-sided checks.
                     None values in records are skipped.

    Returns:
        QualityCheck with:
        - check_name: 'value_ranges'
        - passed: True if all values are within ranges
        - details: Description of out-of-range values
        - affected_count: Number of records with at least one out-of-range value
    """
    # TODO: Implement your solution here
    pass


def run_quality_checks(
    records: List[Dict[str, Any]],
    required_fields: Optional[List[str]] = None,
    unique_fields: Optional[List[str]] = None,
    type_specs: Optional[Dict[str, type]] = None,
    range_specs: Optional[Dict[str, Dict[str, Any]]] = None
) -> QualityReport:
    """
    Run all specified quality checks and return a comprehensive report.

    Args:
        records: List of record dictionaries
        required_fields: Fields to check for completeness (optional)
        unique_fields: Fields to check for uniqueness (optional)
        type_specs: Type specifications (optional)
        range_specs: Value range specifications (optional)

    Returns:
        QualityReport with results from all checks that were requested.
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def _make_test_records() -> List[Dict[str, Any]]:
    """Create test records with various quality issues."""
    return [
        {'id': 1, 'name': 'Alice', 'age': 30, 'salary': 100000.0, 'dept': 'Engineering'},
        {'id': 2, 'name': 'Bob', 'age': 25, 'salary': 85000.0, 'dept': 'Marketing'},
        {'id': 3, 'name': '', 'age': 35, 'salary': 95000.0, 'dept': 'Engineering'},
        {'id': 4, 'name': 'Diana', 'age': -5, 'salary': 110000.0, 'dept': 'Sales'},
        {'id': 4, 'name': 'Eve', 'age': 28, 'salary': 'not_a_number', 'dept': 'Marketing'},
        {'id': 6, 'name': None, 'age': 40, 'salary': 120000.0, 'dept': 'Engineering'},
    ]


def test_check_completeness():
    """Test completeness checking."""
    records = _make_test_records()
    result = check_completeness(records, ['id', 'name'])

    assert not result.passed, "Should fail: records 3 and 6 have empty/null names"
    assert result.affected_count == 2, f"Expected 2 affected records, got {result.affected_count}"

    # All records have 'dept'
    result_dept = check_completeness(records, ['dept'])
    assert result_dept.passed, "All records have dept values"

    print("PASS: Completeness check works correctly")


def test_check_uniqueness():
    """Test uniqueness checking."""
    records = _make_test_records()
    result = check_uniqueness(records, ['id'])

    assert not result.passed, "Should fail: id=4 is duplicated"
    assert result.affected_count == 1, f"Expected 1 duplicate, got {result.affected_count}"

    # Name + dept should be unique
    result_combo = check_uniqueness(records, ['name', 'dept'])
    assert result_combo.passed, "name+dept combinations should be unique"

    print("PASS: Uniqueness check works correctly")


def test_check_type_conformity():
    """Test type conformity checking."""
    records = _make_test_records()
    result = check_type_conformity(records, {'age': int, 'salary': float})

    assert not result.passed, "Should fail: Eve's salary is a string"
    assert result.affected_count == 1, f"Expected 1 type mismatch, got {result.affected_count}"

    print("PASS: Type conformity check works correctly")


def test_check_value_ranges():
    """Test value range checking."""
    records = _make_test_records()

    # Only check records where age is actually an int (skip type-invalid ones)
    valid_records = [r for r in records if isinstance(r.get('age'), int)]
    result = check_value_ranges(valid_records, {'age': {'min': 0, 'max': 150}})

    assert not result.passed, "Should fail: Diana's age is -5"
    assert result.affected_count == 1, f"Expected 1 out-of-range, got {result.affected_count}"

    print("PASS: Value range check works correctly")


def test_full_quality_report():
    """Test full quality report generation."""
    records = _make_test_records()
    report = run_quality_checks(
        records,
        required_fields=['id', 'name'],
        unique_fields=['id'],
        type_specs={'age': int, 'salary': float}
    )

    assert not report.passed, "Overall report should fail"
    assert report.total_records == 6, f"Expected 6 records, got {report.total_records}"

    summary = report.summary
    assert summary['total_checks'] == 3, f"Expected 3 checks, got {summary['total_checks']}"
    assert summary['failed_checks'] >= 2, f"Expected at least 2 failures, got {summary['failed_checks']}"

    print("PASS: Full quality report works correctly")


if __name__ == "__main__":
    test_check_completeness()
    test_check_uniqueness()
    test_check_type_conformity()
    test_check_value_ranges()
    test_full_quality_report()
    print("\nAll tests passed! Great job!")

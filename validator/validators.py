from dataclasses import dataclass
from typing import List, Any


@dataclass
class TestResult:
    success: bool
    message: str
    erroneous_rows: List[Any] = None


def row_count(result, expected_value):
    """
    Assert the number of returned rows.

    Args:
        result (list): Rows returned from the SQL query.
        expected_value (int): The expected number of rows.

    Returns:
        TestResult: Object containing test result.
    """
    count = len(result)
    if count != expected_value:
        return TestResult(
            success=False,
            message=f"Expected {expected_value}, got {count}",
            erroneous_rows=result
        )
    return TestResult(success=True, message="Row count matches expected value")


def has(result, rules):
    """
    Assert existence of specific values in the returned rows.

    Args:
        result (list): Rows returned from the SQL query.
        rules (list): List of expected values in columns.

    Returns:
        TestResult: Object containing test result.
    """
    remaining_rules = []
    erroneous_rows = []

    for rule in rules:
        rule['values'] = set(rule['values'])

    for row in result:
        for rule in rules:
            col_val = getattr(row, rule['column'], None)
            if col_val in rule['values']:
                rule['values'].discard(col_val)
            elif col_val is not None:
                erroneous_rows.append(row)

    remaining_rules = [rule for rule in rules if rule['values']]

    if remaining_rules:
        return TestResult(
            success=False,
            message=f"Expected values not found: {remaining_rules}",
            erroneous_rows=erroneous_rows
        )
    return TestResult(success=True, message="All expected values found")


def missing(result, rules):
    """
    Assert that specific values do not exist in the returned result.

    Args:
        result (list): Rows returned from the SQL query.
        rules (list): List of values that should not be present in columns.

    Returns:
        TestResult: Object containing test result.
    """
    erroneous_rows = []

    for rule in rules:
        rule['values'] = set(rule['values'])

    for row in result:
        for rule in rules:
            col_val = getattr(row, rule['column'], None)
            if col_val in rule['values']:
                erroneous_rows.append(row)

    if erroneous_rows:
        return TestResult(
            success=False,
            message="Unexpected values found",
            erroneous_rows=erroneous_rows
        )
    return TestResult(success=True, message="No unexpected values found")


def no_nulls(result, columns):
    """
    Assert that no null values exist in the specified columns.

    Args:
        result (list): Rows returned from the SQL query.
        columns (list): List of columns that should not contain null values.

    Returns:
        TestResult: Object containing test result.
    """
    erroneous_rows = []

    for row in result:
        for column in columns:
            col_val = getattr(row, column, None)
            if col_val is None:
                erroneous_rows.append(row)
                break

    if erroneous_rows:
        return TestResult(
            success=False,
            message="Unexpected 'null' values found",
            erroneous_rows=erroneous_rows
        )
    return TestResult(success=True, message="No null values found in specified columns")


def only_nulls(result, columns):
    """
    Assert that only null values exist in the specified columns.

    Args:
        result (list): Rows returned from the SQL query.
        columns (list): List of columns that should only contain null values.

    Returns:
        TestResult: Object containing test result.
    """
    erroneous_rows = []

    for row in result:
        for column in columns:
            col_val = getattr(row, column, None)
            if col_val is not None:
                erroneous_rows.append(row)
                break

    if erroneous_rows:
        return TestResult(
            success=False,
            message="Unexpected non-null values found",
            erroneous_rows=erroneous_rows
        )
    return TestResult(success=True, message="Only null values found in specified columns")

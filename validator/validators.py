def row_count(result, expected_value):
    """
    Assert the number of returned rows.

    Args:
        result (list): Rows returned from the SQL query.
        expected_value (int): The expected number of rows.

    Raises:
        AssertionError: If number of rows does not match the expected value.
    """

    count = len(result)
    assert count == expected_value, f"Expected {expected_value}, got {count}"


def has(result, rules):
    """
    Assert existence of specific values in the returned rows.

    Args:
        result (list): Rows returned from the SQL query.
        rules (list): List of expected values in columns.

    Raises:
        AssertionError: If any of the expected values are not found.
    """

    for rule in rules:
        rule['values'] = set(rule['values'])

    for row in result:
        for rule in rules:
            col_val = getattr(row, rule['column'], None)
            if col_val in rule['values']:
                rule['values'].discard(col_val)

    remaining_rules = [rule for rule in rules if rule['values']]

    assert not remaining_rules, f"Expected values not found: {remaining_rules}"


def missing(result, rules):
    """
    Assert that specific values do not exist in the returned result.

    Args:
        result (list): Rows returned from the SQL query.
        rules (list): List of values that should not be present in columns.

    Raises:
        AssertionError: If any of the specified values are found.
    """

    for rule in rules:
        rule['values'] = set(rule['values'])

    for row in result:
        for rule in rules:
            col_val = getattr(row, rule['column'], None)
            assert col_val not in rule['values'], (
                f"Unexpected value '{col_val}' found in column '{rule['column']}'"
            )


def no_nulls(result, columns):
    """
    Assert that no null values exist in the specified columns.

    Args:
        result (list): Rows returned from the SQL query.
        columns (list): List of columns that should not contain null values.

    Raises:
        AssertionError: If any null value is found in the specified columns.
    """

    for row in result:
        for column in columns:
            col_val = getattr(row, column, None)
            assert col_val is not None, (
                f"Unexpected 'null' value in column '{column}'"
            )


def only_nulls(result, columns):
    """
    Assert that only null values exist in the specified columns.

    Args:
        result (list): Rows returned from the SQL query.
        columns (list): List of columns that should only contain null values.

    Raises:
        AssertionError: If non-null value is found in the specified columns.
    """

    for row in result:
        for column in columns:
            col_val = getattr(row, column, None)
            assert col_val is None, (
                f"Unexpected value '{col_val}' in column '{column}'"
            )


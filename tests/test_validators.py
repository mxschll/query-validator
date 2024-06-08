import pytest
from validator import validators


class MockRow:
    """Mock class to simulate a row returned from a SQL query."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_row_count():
    result = [MockRow(id=1), MockRow(id=2), MockRow(id=3)]
    validators.row_count(result, 3)

    with pytest.raises(AssertionError):
        validators.row_count(result, 2)


def test_has():
    result = [
        MockRow(id=1, name='Alice'),
        MockRow(id=2, name='Bob'),
        MockRow(id=3, name='Charlie')
    ]
    rules = [{'column': 'name', 'values': ['Alice', 'Bob']}]
    validators.has(result, rules)

    rules = [{'column': 'name', 'values': ['Alice', 'Dan']}]
    with pytest.raises(AssertionError):
        validators.has(result, rules)


def test_missing():
    result = [
        MockRow(id=1, name='Alice'),
        MockRow(id=2, name='Bob'),
        MockRow(id=3, name='Charlie')
    ]
    rules = [{'column': 'name', 'values': ['Dan', 'Eve']}]
    validators.missing(result, rules)

    rules = [{'column': 'name', 'values': ['Alice', 'Dan']}]
    with pytest.raises(AssertionError):
        validators.missing(result, rules)


def test_no_nulls():
    result = [
        MockRow(id=1, name='Alice'),
        MockRow(id=2, name='Bob'),
        MockRow(id=3, name='Charlie')
    ]
    columns = ['id', 'name']
    validators.no_nulls(result, columns)

    result_with_null = [
        MockRow(id=1, name='Alice'),
        MockRow(id=2, name=None),
        MockRow(id=3, name='Charlie')
    ]
    with pytest.raises(AssertionError):
        validators.no_nulls(result_with_null, columns)


def test_only_nulls():
    result = [
        MockRow(id=None, name=None),
        MockRow(id=None, name=None),
        MockRow(id=None, name=None)
    ]
    columns = ['id', 'name']
    validators.only_nulls(result, columns)

    result_with_non_null = [
        MockRow(id=None, name=None),
        MockRow(id=2, name=None),
        MockRow(id=None, name='Charlie')
    ]
    with pytest.raises(AssertionError):
        validators.only_nulls(result_with_non_null, columns)


if __name__ == "__main__":
    pytest.main()

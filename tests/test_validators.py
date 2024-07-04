
import pytest
from validator import validators


class MockRow:
    """Mock class to simulate a row returned from a SQL query."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if not isinstance(other, MockRow):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"MockRow({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())})"


@pytest.fixture
def sample_data():
    return [
        MockRow(id=1, name='Alice'),
        MockRow(id=2, name='Bob'),
        MockRow(id=3, name='Charlie')
    ]


class TestRowCount:
    @pytest.mark.parametrize("expected_count,should_succeed", [
        (3, True),
        (2, False)
    ])
    def test_row_count(self, sample_data, expected_count, should_succeed):
        """
        Test the row_count validator with different expected counts.
        """
        validator_result = validators.row_count(sample_data, expected_count)
        assert validator_result.success is should_succeed
        assert (validator_result.erroneous_rows is None) == should_succeed
        if not should_succeed:
            assert validator_result.erroneous_rows == sample_data


class TestHas:
    @pytest.mark.parametrize("rules,should_succeed,expected_erroneous", [
        ([{'column': 'name', 'values': ['Alice', 'Bob']}], True, None),
        ([{'column': 'name', 'values': ['Alice', 'Dan']}], False, [
         MockRow(id=2, name='Bob'), MockRow(id=3, name='Charlie')])
    ])
    def test_has(self, sample_data, rules, should_succeed, expected_erroneous):
        """
        Test the has validator with different rules.
        """
        validator_result = validators.has(sample_data, rules)
        assert validator_result.success is should_succeed
        assert validator_result.erroneous_rows == expected_erroneous


class TestMissing:
    @pytest.mark.parametrize("rules,should_succeed,expected_erroneous", [
        ([{'column': 'name', 'values': ['Dan', 'Eve']}], True, None),
        ([{'column': 'name', 'values': ['Alice', 'Dan']}],
         False, [MockRow(id=1, name='Alice')])
    ])
    def test_missing(self, sample_data, rules, should_succeed, expected_erroneous):
        """
        Test the missing validator with different rules.
        """
        validator_result = validators.missing(sample_data, rules)
        assert validator_result.success is should_succeed
        assert validator_result.erroneous_rows == expected_erroneous


class TestNulls:
    @pytest.fixture
    def sample_data_with_null(self):
        return [
            MockRow(id=1, name='Alice'),
            MockRow(id=2, name=None),
            MockRow(id=3, name='Charlie')
        ]

    COLUMNS = ['id', 'name']

    def test_no_nulls_success(self, sample_data):
        """
        Test the no_nulls validator when there are no null values.
        """
        validator_result = validators.no_nulls(sample_data, self.COLUMNS)
        assert validator_result.success is True
        assert validator_result.erroneous_rows is None

    def test_no_nulls_failure(self, sample_data_with_null):
        """
        Test the no_nulls validator when there are null values.
        """
        validator_result = validators.no_nulls(
            sample_data_with_null, self.COLUMNS)
        assert validator_result.success is False
        assert validator_result.erroneous_rows == [MockRow(id=2, name=None)]

    @pytest.fixture
    def all_null_data(self):
        return [MockRow(id=None, name=None)] * 3

    def test_only_nulls_success(self, all_null_data):
        """
        Test the only_nulls validator when all values are null.
        """
        validator_result = validators.only_nulls(all_null_data, self.COLUMNS)
        assert validator_result.success is True
        assert validator_result.erroneous_rows is None

    def test_only_nulls_failure(self, sample_data_with_null):
        """
        Test the only_nulls validator when not all values are null.
        """
        validator_result = validators.only_nulls(
            sample_data_with_null, ['name'])
        assert validator_result.success is False
        assert validator_result.erroneous_rows == [
            MockRow(id=1, name='Alice'), MockRow(id=3, name='Charlie')]


if __name__ == "__main__":
    pytest.main()

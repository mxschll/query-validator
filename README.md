# Query Validator

This project aims to provide an easy way to automatically validate the output of SQL queries.

## Test Definition

```yaml filename="test-select-users.yaml"
query: |
  SELECT id, username, email, created_at, deleted_at
  FROM users
  WHERE created_at > :date_today
assertions:
  count: 5  # Expecting 5 rows in the result
  has:
    - column: "email"
      values: 
        - "bob@example.com"
        - "alice@example.com"
    - column: "username"
      values: 
        - "alice"
        - "bob"
  missing:
    - column: "email"
      values: 
        - "sally@example.com"
    - column: "username"
      values:
        - "sally"
      regex:
        - "^admin.*"  # No usernames starting with 'admin'
  conditions:
    - column: "created_at"
      operator: ">"
      value: ":current_date"
    - column: "id"
      operator: ">"
      value: 1000
  no_nulls:
    - column: "email"
  only_nulls:
    - column: "deleted_at"
```

### Keys Explanation

| Key          | Description                                               | Values                                          |
| :----------- | :-------------------------------------------------------- | :---------------------------------------------- |
| `query`      | The SQL query to be executed.                             | A valid SQL query string.                       |
| `assertions` | A collection of assertions to validate the query results. | A dictionary containing assertions (see below). |

### `assertions`

| Key                     | Description                                                  | Values                                                       |
| :---------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| `assertions.count`      | The expected number of rows in the result set.               | An integer representing the expected row count.              |
| `assertions.has`        | Assertions to check for the presence of specific values in the result set. | A list of dictionaries, each containing: `column` and `values`. |
| `assertions.missing`    | Assertions to check for the absence of specific values in the result set. | A list of dictionaries, each containing: `column`, `values`, and optional `regex`. |
| `assertions.conditions` | Assertions to check for specific conditions on the result set. | A list of dictionaries, each containing: `column`, `operator`, and `value`. |
| `assertions.no_nulls` | Assertions to check that there are no null values in the specified columns. |  |
| `assertions.only_nulls` | Assertions to that there are only null values in the specified columns. |  |

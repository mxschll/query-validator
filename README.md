# Query Validator

This project aims to provide an easy way to automatically validate the output of SQL queries.


## Example Test

```yaml filename="test-select-users.yaml"
query: |
  SELECT id, username, email, created_at
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
```

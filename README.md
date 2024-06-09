# Query Validator

This project provides an easy way to automatically validate the output of SQL queries.

## Test Definition

Tests for SQL query result sets are defined in YAML files. You can write multiple assertions for one query, but it's advisable to split assertions into several test files. Currently, one failing assertion stops the entire test.

The format is as follows:

```yaml filename="test-select-users.yaml"
query: | # The query to be executed. Assertions are run on the result set.
  SELECT id, username, email, created_at, deleted_at
  FROM users
assertions:
  count: 5  # Expecting 5 rows in the result.
  has: # Values must exist (at least once) in specified column.
    - column: "email"
      values: 
        - "bob@example.com"
        - "alice@example.com"
    - column: "username"
      values: 
        - "alice"
        - "bob"
  missing: # Values must not exist in specified column.
    - column: "email"
      values: 
        - "sally@example.com"
    - column: "username"
      values:
        - "sally"
  no_nulls: ["email"] # Columns must not have null values.
  only_nulls: ["deleted_at"] # Columns must only have null values.
```

## Configuration

- `DB_URI`
- `TEST_FILES` 
- `LOG_LEVEL`
- `LOG_TO_CONSOLE`
- `LOG_FILE_PATH`
- `LOKI_HOST`
- `LOKI_USERNAME`
- `LOKI_PASSWORD`
- `LOKI_TAGS`

## Docker

### How to use this image

#### Starting using minimal configuration

Mount the directory with your test files into the container at `/app/queries`. Specify the `DB_URL` pointing to the host and database, and set `CRON_SCHEDULE` for periodic test runs.

```bash
docker run --detach --name my-query-validator \
	--volume "$(pwd)/queries:/app/queries" \
	--env "DB_URL=postgresql://username:password@dbhost:5432/dbname" \
	--env "CRON_SCHEDULE=*/5 * * * *" \
	query-validator:latest
```

To attach the container to an existing Docker network:

```bash
docker run --detach --name my-query-validator \
	--volume "$(pwd)/queries:/app/queries" \
	--env "DB_URL=postgresql://username:password@dbhost:5432/dbname" \
	--env "CRON_SCHEDULE=*/5 * * * *" \
	--network database-network-name 
	query-validator:latest
```

Retrieve container logs:

```bash
docker logs -f my-query-validator
```


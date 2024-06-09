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

The program can be configured via a `.env` file or by passing environment variables to the Docker container (see section [Docker](#Docker)).

- `DB_URI` (required): The database connection URI.
- `TEST_FILES` (required): Path to the test files. When running via Docker, this path is reflected inside the container. When running the Python script outside Docker, the path is relative to the location where the script is run, or you can specify an absolute path.
- `LOG_FILE_PATH` (optional): Path to the log file. When omitted, no log file is written.
- `LOKI_HOST` (optional): The Loki host for logging.
- `LOKI_USERNAME` (optional): The Loki username.
- `LOKI_PASSWORD` (optional): The Loki password.
- `LOKI_TAGS` (optional): Tags for Loki logging.

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

#### Docker Compose

```yaml
services:
  db:
    image: postgres
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: username 
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase

  validator:
    image: query-validator
    restart: unless-stopped
    environment:
      DB_URL: "postgresql://username:password@db:5432/mydatabase"
      LOKI_HOST: 'http://loki:3100/loki/api/v1/push' # Send logs to Loki
      CRON_SCHEDULE: "*/5 * * * *"
    volumes:
      - ./queries:/app/queries

  loki:
    image: grafana/loki:2.9.2
    ports:
      - "3100:3100"

  grafana:
    environment:
      - GF_PATHS_PROVISIONING=/etc/grafana/provisioning
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    entrypoint:
      - sh
      - -euc
      - |
        mkdir -p /etc/grafana/provisioning/datasources
        cat <<EOF > /etc/grafana/provisioning/datasources/ds.yaml
        apiVersion: 1
        datasources:
        - name: Loki
          type: loki
          access: proxy 
          orgId: 1
          url: http://loki:3100
          basicAuth: false
          isDefault: true
          version: 1
          editable: false
        EOF
        /run.sh
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```


import time
import config
import logger
import loader
import database
import validators
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_assertions(rows, assertions):
    """
    Run a series of assertions on the result set.

    Args:
        rows (list): List of rows returned from the SQL query.
        assertions (dict): Dictionary of assertions to apply to the result set.

    Raises:
        AssertionError: If any of the assertions fail.
        ValueError: If an unknown assertion is encountered.
    """

    assertion_map = {
        'count': validators.row_count,
        'has': validators.has,
        'missing': validators.missing,
        'no_nulls': validators.no_nulls,
        'only_nulls': validators.only_nulls
    }

    for key, assertion in assertions.items():
        if key in assertion_map:
            try:
                assertion_map[key](rows, assertion)
            except AssertionError as e:
                raise AssertionError(
                    f"Assertion '{key}' failed: {str(e)}") from e
        else:
            raise ValueError(f"Unknown assertion '{key}'")


def execute_test(test, db_url):
    start_time = time.time()
    name = test.get('name')
    query = test.get('query')
    assertions = test.get('assertions', {})
    result_status = 'PASS'
    error_message = ''
    rows = []

    try:
        engine = database.create_db_engine(db_url)
        result = database.execute_query(engine, query)
        rows = result.all()

        run_assertions(rows, assertions)

    except AssertionError as e:
        result_status = 'FAIL'
        error_message = str(e)

    except Exception as e:
        result_status = 'ERROR'
        error_message = str(e)

    duration = time.time() - start_time

    return {
        'name': name,
        'status': result_status,
        'duration': duration,
        'error_message': error_message,
        'assertions': assertions,
        'query': query,
        'data': [tuple(row) for row in rows]
    }


def main():
    """Main function to execute the tests and log the results."""

    cfg = config.settings

    test_files = loader.load_test_files(cfg['TEST_FILES'])
    engine = database.create_db_engine(cfg['DB_URL'])
    logger.setup_logging(cfg)

    summary = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'details': []
    }

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(execute_test, test, cfg['DB_URL'])
                   for test in test_files]

        for future in as_completed(futures):
            result = future.result()
            summary['total'] += 1
            if result['status'] == 'PASS':
                summary['passed'] += 1
            elif result['status'] == 'FAIL':
                summary['failed'] += 1
            else:
                summary['errors'] += 1

            summary['details'].append(result)
            logger.log_test_result(
                result['name'],
                result['status'],
                result['duration'],
                result['query'],
                result['data'],
                result['error_message'])

    end_time = time.time()
    summary['runtime'] = end_time - start_time

    engine.dispose()
    logger.log_summary(summary)


if __name__ == '__main__':
    main()

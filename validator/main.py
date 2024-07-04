import time
import config
import logger
import loader
import database
import validators
from validators import TestResult
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_assertions(rows, assertions):
    """
    Run a series of assertions on the result set.

    Args:
        rows (list): List of rows returned from the SQL query.
        assertions (dict): Dictionary of assertions to apply to the result set.

    Returns:
        list: List of TestResult objects for failed assertions.
    """

    assertion_map = {
        'count': validators.row_count,
        'has': validators.has,
        'missing': validators.missing,
        'no_nulls': validators.no_nulls,
        'only_nulls': validators.only_nulls
    }

    failed_assertions = []

    for key, assertion in assertions.items():
        if key in assertion_map:
            result = assertion_map[key](rows, assertion)
            if not result.success:
                failed_assertions.append((key, result))
        else:
            failed_assertions.append(
                (key, TestResult(False, f"Unknown assertion '{key}'")))

    return failed_assertions


def execute_test(test, db_url):
    start_time = time.time()
    name = test.get('name')
    query = test.get('query')
    assertions = test.get('assertions', {})
    result_status = 'PASS'
    error_messages = []
    erroneous_rows = []
    rows = []

    try:
        engine = database.create_db_engine(db_url)
        result = database.execute_query(engine, query)
        rows = result.all()

        failed_assertions = run_assertions(rows, assertions)

        if failed_assertions:
            result_status = 'FAIL'
            for key, test_result in failed_assertions:
                error_messages.append(
                    f"Assertion '{key}' failed: {test_result.message}")
                if test_result.erroneous_rows:
                    erroneous_rows.extend(test_result.erroneous_rows)

    except Exception as e:
        result_status = 'ERROR'
        error_messages.append(str(e))

    duration = time.time() - start_time

    return {
        'name': name,
        'status': result_status,
        'duration': duration,
        'error_messages': error_messages,
        'erroneous_rows': erroneous_rows,
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
                result['error_messages'],
                result['erroneous_rows'])

    end_time = time.time()
    summary['runtime'] = end_time - start_time

    engine.dispose()
    logger.log_summary(summary)


if __name__ == '__main__':
    main()

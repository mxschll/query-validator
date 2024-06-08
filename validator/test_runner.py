import time
import config
import logger
import logging
import database
import test_loader
import validators


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


def main():
    """Main function to execute the tests and log the results."""
    logger.setup_logging()
    test_files = test_loader.load_test_files()

    try:
        cfg = config.load_config()
    except ValueError as e:
        logging.error(f"Config Error: {e}")
        exit(1)

    engine = database.create_db_engine(cfg['DB_URI'])

    summary = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'details': []
    }

    for test in test_files:
        start_time = time.time()
        name = test.get('name')
        query = test.get('query')
        assertions = test.get('assertions', {})
        result_status = 'PASS'
        error_message = ''

        try:
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
        logger.log_test_result(name, result_status, duration, error_message)

        summary['total'] += 1
        if result_status == 'PASS':
            summary['passed'] += 1
        elif result_status == 'FAIL':
            summary['failed'] += 1
        else:
            summary['errors'] += 1

        summary['details'].append({
            'name': name,
            'status': result_status,
            'duration': duration,
            'error_message': error_message,
            'assertions': assertions
        })

    engine.dispose()
    logger.log_summary(summary)


if __name__ == '__main__':
    main()

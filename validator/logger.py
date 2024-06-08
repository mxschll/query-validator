import logging


def setup_logging():
    """Set up logging configuration."""
    file_handler = logging.FileHandler('logs/test_results.log')
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'))
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'))

    logging.basicConfig(
        handlers=[file_handler, console_handler],
        level=logging.INFO
    )


def log_test_result(test_name, result, duration, error=None):
    """Log the result of a test case."""
    if result == 'PASS':
        logging.info(f"Test: {test_name}, "
                     f"Result: {result}, "
                     f"Duration: {duration: .2f} seconds")
    else:
        logging.error(f"Test: {test_name}, Result: {result}, Duration: {
                      duration:.2f} seconds, Error: {error}")


def log_summary(summary):
    """Log a summary of all test results."""
    print("\nTest Summary")
    print("============")
    print(f"Tests:  {summary['total']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Errors: {summary['errors']}\n")
    for detail in summary['details']:
        print(f"Test: {detail['name']}")
        print(f"  Status: {detail['status']}")
        print(f"  Duration: {detail['duration']:.2f} seconds")
        if detail['error_message']:
            print(f"  Error: {detail['error_message']}")
        print("")

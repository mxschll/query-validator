import logging
import logging_loki


def setup_logging(config):
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, config['LOG_LEVEL']))

    handlers = []

    # Console handler
    if config['LOG_TO_CONSOLE']:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config['LOG_LEVEL']))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)

    # File handler
    if config['LOG_TO_FILE']:
        file_handler = logging.FileHandler(config['LOG_FILE_PATH'])
        file_handler.setLevel(getattr(logging, config['LOG_LEVEL']))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    # Loki handler
    if config['LOKI_HOST']:
        loki_handler = logging_loki.LokiHandler(
            url=config['LOKI_HOST'],
            tags=dict(tag.split('=')
                      for tag in config['LOKI_TAGS'].split(',')),
            auth=(config['LOKI_USERNAME'], config['LOKI_PASSWORD']),
            version="1",
        )
        loki_handler.setLevel(getattr(logging, config['LOG_LEVEL']))
        handlers.append(loki_handler)

    logging.basicConfig(handlers=handlers, level=getattr(
        logging, config['LOG_LEVEL']))


def log_test_result(test_name, result, duration, error=None):
    """Log the result of a test case."""
    if result == 'PASS':
        logging.info(f"Test: {test_name}, "
                     f"Result: {result}, "
                     f"Duration: {duration: .2f} seconds")
    else:
        logging.error(f"Test: {test_name}, "
                      f"Result: {result}, "
                      f"Duration: {duration:.2f} seconds, "
                      f"Error: {error}")


def log_summary(summary):
    """Log a summary of all test results."""
    logging.info(f"SUMMARY - "
                 f"Tests: {summary['total']}, "
                 f"Passed: {summary['passed']}, "
                 f"Failed: {summary['failed']}, "
                 f"Errors: {summary['errors']}")

import logging
import logging_loki
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = self.create_log_record(record)

        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)

        extra_fields = self.get_extra_fields(record)
        log_record.update(extra_fields)

        return json.dumps(log_record)

    def create_log_record(self, record):
        return {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
        }

    def get_extra_fields(self, record):
        standard_fields = {
            'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
            'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
            'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
            'thread', 'threadName', 'processName', 'process', 'asctime',
            'taskName'
        }

        return {key: value for key, value in record.__dict__.items()
                if key not in standard_fields}


def setup_logging(config):
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, config['LOG_LEVEL']))

    handlers = []

    json_formatter = JsonFormatter()

    # Console handler
    if config['LOG_TO_CONSOLE']:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config['LOG_LEVEL']))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)

    # File handler
    if config['LOG_FILE_PATH']:
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
        loki_handler.setFormatter(json_formatter)
        handlers.append(loki_handler)

    logging.basicConfig(handlers=handlers, level=getattr(
        logging, config['LOG_LEVEL']))


def log_test_result(test_name, test_result, duration, query, error_msg, err):
    """Log the result of a test case."""

    message = (f"Test: {test_name}, "
               f"Result: {test_result}, "
               f"Duration: {duration:.2f} seconds")

    if test_result == 'PASS':
        logging.info(message)
    else:
        logging.error(message, extra={
            'assertions': error_msg,
            'errornous_rows': [dict(row._mapping) for row in err],
            'query': query})


def log_summary(summary):
    """Log a summary of all test results."""

    message = (f"SUMMARY - "
               f"Tests: {summary['total']}, "
               f"Passed: {summary['passed']}, "
               f"Failed: {summary['failed']}, "
               f"Errors: {summary['errors']}")

    logging.info(message)

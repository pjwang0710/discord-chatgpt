import os
import logging
import logging.handlers


class CustomFormatter(logging.Formatter):
    __LEVEL_COLORS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]
    __FORMATS = None

    @classmethod
    def get_formats(cls):
        if cls.__FORMATS is None:
            cls.__FORMATS = {
                level: logging.Formatter(
                    f'\x1b[30;1m%(asctime)s\x1b[0m {color}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m -> %(message)s',
                    '%Y-%m-%d %H:%M:%S'
                )
                for level, color in cls.__LEVEL_COLORS
            }
        return cls.__FORMATS

    def format(self, record):
        formatter = self.get_formats().get(record.levelno)
        if formatter is None:
            formatter = self.get_formats()[logging.DEBUG]
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)
        record.exc_text = None
        return output


class LoggerFactory:
    _logger = None

    @classmethod
    def create_logger(cls, formatter):
        if cls._logger is None:
            cls._logger = Logger(formatter)
        return cls._logger


class Logger:
    def __init__(self, formatter):
        self.logger = logging.getLogger('chatgpt_logger')
        self.logger.setLevel(logging.INFO)
        self.formatter = formatter

    def add_handler(self, handler):
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def logging_to_file(self, log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        self.add_handler(file_handler)

    def logging_to_console(self):
        console_handler = logging.StreamHandler()
        self.add_handler(console_handler)


formatter = CustomFormatter()
logger = LoggerFactory.create_logger(formatter)
logger.logging_to_file('./logs')
logger.logging_to_console()

import logging
import os
from datetime import datetime
import inspect

COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_RESET = '\033[0m'
COLOR_BLUE = '\033[94m'
COLOR_GREY = '\033[90m'


class CustomFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        message = record.getMessage()
        
        if levelname == 'DEBUG':
            levelname_color = COLOR_BLUE
            message_color = COLOR_GREEN
        elif levelname == 'INFO':
            levelname_color = COLOR_BLUE
            message_color = COLOR_GREEN
        elif levelname == 'WARNING':
            levelname_color = COLOR_YELLOW
            message_color = COLOR_YELLOW
        elif levelname == 'ERROR':
            levelname_color = COLOR_RED
            message_color = COLOR_RED
        elif levelname == 'CRITICAL':
            levelname_color = COLOR_RED
            message_color = COLOR_RED
        else:
            levelname_color = ''
            message_color = ''
        
        timestamp = self.formatTime(record, self.datefmt)
        levelname_formatted = f'{levelname_color}{levelname:<8}{COLOR_RESET}'
        formatted_message = f'{COLOR_GREY}{timestamp} {levelname_formatted} {message_color}{message}{COLOR_RESET}'
        return formatted_message
class DailyFileHandler(logging.FileHandler):
    def __init__(self, directory, mode='a', encoding=None, delay=False):
        self.directory = directory
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self.current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self.date_time = datetime.now().strftime("%Y-%m-%d")
        filename = self._get_filename()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        super().__init__(filename, mode, encoding, delay)

    def _get_filename(self):
        return os.path.join(self.directory, f"{self.current_datetime}.log")

    def emit(self, record):
        new_datetime = datetime.now().strftime("%Y-%m-%d")
        if new_datetime != self.date_time:
            self.current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            self.date_time = new_datetime
            filename = self._get_filename()
            self.baseFilename = filename
            self.stream = self._open()
        super().emit(record)


logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
color_formatter = CustomFormatter(datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(color_formatter)
console_handler.setLevel(logging.DEBUG)


file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
daily_file_handler = DailyFileHandler(directory='./logs', encoding='utf-16')
daily_file_handler.setLevel(logging.DEBUG)
daily_file_handler.setFormatter(file_formatter)
logger.addHandler(daily_file_handler)
logger.addHandler(console_handler)

discord_logger = logging.getLogger('discord')
discord_logger.addHandler(console_handler)

def console_log(message, status):
    frame = inspect.currentframe()
    outer_frame = inspect.getouterframes(frame)
    caller_frame_record = outer_frame[1]
    caller_line_no = caller_frame_record.lineno
    
    if status == "info":
        logger.info(message)
    elif status == "error":
        message += f" at line {caller_line_no}"
        logger.error(message)
    elif status == "warning":
        logger.warning(message)
    else:
        logger.debug(message)
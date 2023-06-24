import logging
import sys
import datetime
from pathlib import Path
from typing import Union


def get_current_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H.%M.%S")


def create_log_file_and_dir(app_name) -> Union[Path, None]:
    home_dir = Path.home()
    log_file = home_dir.joinpath(f".{app_name}/{app_name}_{get_current_timestamp()}.log")
    log_file.parent.mkdir(exist_ok=True, parents=True)
    if log_file.parent.exists():
        print(f"Log directory created: {log_file.parent}")
        return log_file
    else:
        print(f"Failed to create log directory: {log_file.parent}")
        return None


def setup_logging(log_to_file=False, level=logging.DEBUG):
    # Create the root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create a formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -- %(message)s")

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_to_file:
        # Create a file handler
        log_file = create_log_file_and_dir
        if log_file:
            file_handler = logging.FileHandler(str(log_file))
            # file_handler = logging.FileHandler(f'twedit++_{get_current_timestamp()}.log')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    # Return the logger
    return logger


# Example usage
logger = setup_logging(log_to_file=False, level=logging.DEBUG)


def get_logger(name="logger"):
    return logging.getLogger(name)
    # return logger


# # Log messages
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')

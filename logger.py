import logging
import sys
from colorlog import ColoredFormatter

# get logger
logger = logging.getLogger()
# create formatter
# formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
# create colored formatter
formatter = ColoredFormatter(
    fmt="%(bold_purple)s%(asctime)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(bold_light_white)s%(message)s%(reset)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
# create handlers
stream_handler = logging.StreamHandler(sys.stdout)
# file_handler = logging.FileHandler("app.log")
# set formatters
stream_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)
# add handlers to the logger
logger.handlers = [stream_handler]
# set log level
logger.setLevel(logging.INFO)

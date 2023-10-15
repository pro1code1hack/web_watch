import logging
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Define a format for the log messages
log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Set up loggers to log to different files
loggers = {
    "api": logging.getLogger("api"),
    "parser": logging.getLogger("parser"),
    # ... add other loggers as needed during further implementation
}

loggers["api"].setLevel(logging.INFO)
loggers["parser"].setLevel(logging.INFO)

# Set up file handlers for each logger
api_handler = logging.FileHandler("logs/api.log")
api_handler.setFormatter(log_format)  # Set the format for this handler

parser_handler = logging.FileHandler("logs/parser.log")
parser_handler.setFormatter(log_format)  # Set the format for this handler

loggers["api"].addHandler(api_handler)
loggers["parser"].addHandler(parser_handler)

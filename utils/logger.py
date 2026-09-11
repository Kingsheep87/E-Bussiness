# @Author: Sheep Wang
# @File: logger.py
# @Created: 2026-09-11 22:10
# @Description: logger.py


import logging
import os
from logging.handlers import RotatingFileHandler




# Define and create logs directory relative to project root
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure log format: [Timestamp] LEVEL in filename:lineno: message
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d: %(message)s"
)

# Initialize global logger
logger = logging.getLogger("e_business_logger")
logger.setLevel(logging.INFO)

# 1. Console Handler (outputs logs to terminal)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 2. Rotating File Handler (max 5MB per log file, keeps up to 3 backups)
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
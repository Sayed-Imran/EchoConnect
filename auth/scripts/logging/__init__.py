import os
import logging
from logging.handlers import RotatingFileHandler
from scripts.config import SERVERConf

logger = logging.getLogger()

logger.setLevel(SERVERConf.log_level)
if not os.path.exists("logs"):
    os.makedirs("logs")
log_file = os.path.join("logs", f"{SERVERConf.module_name}.log")
log_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
logger.addHandler(log_handler)

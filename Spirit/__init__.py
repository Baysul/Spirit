import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Spirit")

universalHandler = RotatingFileHandler("spirit.log", maxBytes=20480, backupCount=3, encoding="utf-8")
logger.addHandler(universalHandler)

errorHandler = logging.FileHandler("error.log")
errorHandler.setLevel(logging.ERROR)
logger.addHandler(errorHandler)
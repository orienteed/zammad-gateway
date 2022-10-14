import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists("logs/tmp"):
    os.makedirs("logs/tmp")

file_name = "logs/tmp/zammad-gateway.log"

logger = logging.getLogger("Zammad_logger")
logger.setLevel(logging.INFO)

# add a rotating handler
handler = RotatingFileHandler(file_name, maxBytes=1000000, backupCount=6)
logger.addHandler(handler)

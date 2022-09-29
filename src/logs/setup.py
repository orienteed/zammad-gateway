import logging
import time
from logging.handlers import RotatingFileHandler


log_file = "zammad-gateway.log"

logger = logging.getLogger("Zammad_logger")
logger.setLevel(logging.INFO)

# add a rotating handler
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=6)
logger.addHandler(handler)

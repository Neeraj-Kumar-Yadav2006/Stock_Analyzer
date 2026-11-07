import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR="logs"

LOG_FILE=os.path.join(LOG_DIR,"app.log")

os.makedirs(LOG_DIR,exist_ok=True)

logger = logging.getLogger("FinancialSystem")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


import logging
import os
from datetime import datetime


current_date = datetime.now()
logs_folder = os.path.join(os.getcwd(), "logs", current_date.strftime("%Y-%m-%d"))
os.makedirs(logs_folder, exist_ok=True)

log_filename = os.path.join(logs_folder, f"{current_date.strftime("%H-%M-%S")}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename)
        # logging.StreamHandler()
    ]
)

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

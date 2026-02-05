import logging
import sys
from pathlib import Path

def setup_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    file_handler = logging.FileHandler(log_dir / "errors.log", encoding="utf-8", mode="a")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    root_logger.handlers = []
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    logging.info("Логгер успешно настроен.")
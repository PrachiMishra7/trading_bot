import logging
import os
from datetime import datetime


def setup_logging(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Logging started → %s", log_file)
    return logger
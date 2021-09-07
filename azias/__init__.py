import logging


def get_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname).3s - %(name)s > %(message)s")
    formatter.datefmt = "%Y/%m/%d %I:%M:%S"
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

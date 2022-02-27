# Imports
import logging
import sys


# Methods
def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Creates a logger with the given attributes and a standard formatter format.
    
    :param name: Name of the logger.
    :param level: Logging level used by the logger.
    :return: The newly or previously created Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Simple check that prevents a logger from having more than one formatter when using the method.
    if len(logger.handlers) == 0:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        # formatter = logging.Formatter("%(asctime)s - %(levelname).3s - %(name)s > %(message)s")
        # formatter.datefmt = "%Y/%m/%d %I:%M:%S"
        formatter = logging.Formatter("[%(asctime)s] [%(name)s/%(levelname).3s]: %(message)s")
        formatter.datefmt = "%H:%M:%S"
        ch.setFormatter(formatter)
        ch.setStream(sys.stdout)
        logger.addHandler(ch)
    
    return logger

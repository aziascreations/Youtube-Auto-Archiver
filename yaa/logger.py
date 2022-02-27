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


def get_human_ms_delay(delay_ms: int) -> str:
    time_string = ""
    
    if delay_ms < 0:
        raise ValueError("The 'delay_ms' parameter should be a positive integer or zero !")
    
    if delay_ms >= 86400000:
        day_count = int(delay_ms / 86400000)
        time_string = time_string + str(day_count) + "d "
        delay_ms = delay_ms - (day_count * 86400000)
    
    if delay_ms >= 3600000:
        hour_count = int(delay_ms / 3600000)
        time_string = time_string + str(hour_count) + "h "
        delay_ms = delay_ms - (hour_count * 3600000)
    
    if delay_ms >= 60000:
        minute_count = int(delay_ms / 60000)
        time_string = time_string + str(minute_count) + "m "
        delay_ms = delay_ms - (minute_count * 60000)
    
    if delay_ms >= 1000:
        second_count = int(delay_ms / 1000)
        time_string = time_string + str(second_count) + "s "
        delay_ms = delay_ms - (second_count * 1000)
    
    if delay_ms > 0:
        time_string = time_string + str(delay_ms) + "ms"
    
    return time_string.strip()

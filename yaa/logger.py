# Imports
import logging
import sys


# Methods
def get_logger(name: str, level: int, log_format: str, log_date_format: str) -> logging.Logger:
    """
    Creates a logger with the given attributes and a standard formatter format.
    
    :param name: Name of the logger.
    :param level: Logging level used by the logger.
    :param log_format: ???
    :param log_date_format: ???
    :return: The newly or previously created Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if len(logger.handlers) == 0:
        # Making sure we don't duplicate the formatter.
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(log_format)
        formatter.datefmt = log_date_format
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

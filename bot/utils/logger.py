"""Makes the logger for the program"""
import logging


def make_logger(name: str, log_level: str) -> logging.Logger:
    """Make Logger

    Creates the logger that is used by the bot. The datahanlder makes it own log

    :param name: Name of logger
    :type name: str
    :param log_level: Logging level. Valid strings are 'DEBUG', 'INFO', 'WARNING',
            'ERROR', 'CRITICAL'
    :type log_level: st
    :return: Logger class that handled the logging.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    fh = logging.FileHandler("{}.log".format(name), mode="w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

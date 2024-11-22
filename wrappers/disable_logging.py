from utils.logger import logging, logger


def disable_logging(f):
    def wrapper(*args):
        logging.disable(logging.CRITICAL)
        try:
            result = f(*args)
        finally:
            logging.disable(logging.NOTSET)
        return result
    return wrapper
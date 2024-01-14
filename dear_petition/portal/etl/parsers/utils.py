from functools import wraps
import logging


logger = logging.getLogger(__name__)


def catch_parse_error(func):
    """Decorator to catch parsing errors so parsing may continue"""

    @wraps(func)
    def wrapper(soup):
        try:
            return func(soup)
        except Exception:
            logger.exception(f"Exception occurred parsing: {soup}")

    return wrapper

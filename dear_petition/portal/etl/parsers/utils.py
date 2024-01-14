from functools import wraps
import logging


logger = logging.getLogger(__name__)


def catch_parse_error(func):
    """Decorator to catch parsing errors so parsing may continue"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception(f"Exception occurred in {args}")

    return wrapper

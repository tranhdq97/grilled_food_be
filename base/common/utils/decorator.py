import logging

logger = logging.getLogger(__name__)


def log(func):
    func_name = func.__name__

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(f"{func_name}")
        logger.debug(f'{func_name} | args: {locals().get("args")} | kwargs: {locals().get("kwargs")}')
        return result

    return inner

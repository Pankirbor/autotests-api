import logging


def get_logger(name: str) -> logging.Logger:
    """
    Функция для получения логгера с заданным именем и
      настройками StreamHeandler, logging.DEBUG.

    Args:
        name (str): Имя логгера.

    Returns:
        logging.Logger: настроенный логгер.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

import logging


def init_logging() -> None:
    logging.basicConfig(level=logging.INFO)
    console_handler = logging.StreamHandler()

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Set the level for the root logger

    # Add the handler to the root logger
    root_logger.addHandler(console_handler)

import logging, os


def setup_logging():
    # Configure logging
    logging.basicConfig(
        filename="app.log",  # Log file name
        level=logging.DEBUG,  # Minimum logging level
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",  # Log message format
    )

    logging.info("Started application.")


def clear_logs():
    # Delete log file
    if os.path.exists("app.log"):
        os.remove("app.log")

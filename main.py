from logger import setup_logging, clear_logs
from utils import populate_default_data
from menu_manager import cli_menu


if __name__ == "__main__":
    clear_logs()
    setup_logging()
    populate_default_data()
    cli_menu()

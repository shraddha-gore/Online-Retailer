from database import Database
from user_manager import UserManager
import logging

db = Database.get_instance()


class AdminManager:
    @staticmethod
    def toggle_security(current_user):
        """Toggles security if the user has admin privileges."""
        try:
            if UserManager.check_if_admin(current_user):
                db.security_enabled = not db.security_enabled  # Toggles security
                status = "ON" if db.security_enabled else "OFF"
                print(f"\nSecurity is now {status}.")
                logging.info(
                    f"User '{current_user}' changed security switched {status} security."
                )
        except Exception as e:
            logging.error(f"An error occurred while toggling security: {e}")
            print("\nAn error occurred while toggling security.")

    @staticmethod
    def view_logs(current_user):
        """View logs if the user has admin privileges."""
        try:
            if UserManager.check_if_admin(current_user):
                logging.info(f"User '{current_user}' requested logs.")
                with open("app.log", "r") as log_file:
                    logs = log_file.read()
                    print("\n--- Application Logs ---")
                    print(logs)
                    print("\n------------------------")
        except FileNotFoundError:
            logging.error("Log file not found.")
            print("\nLog file not found.")
        except Exception as e:
            logging.error(f"An error occurred while accessing the log file: {e}")
            print("\nAn error occurred while accessing the log file.")

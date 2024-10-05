from database import Database
from user import User
import logging
import subprocess
import os
import time

db = Database.get_instance()


def populate_default_data():
    """Populate default users and products."""
    try:
        # Add default users
        db.execute(
            "INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            ("admin", User.hash_password("admin"), True),
        )
        db.execute(
            "INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            ("test", User.hash_password("test123"), False),
        )

        # Add default products
        db.execute(
            "INSERT OR IGNORE INTO products (name, price) VALUES (?, ?)",
            ("Laptop", 1000),
        )
        db.execute(
            "INSERT OR IGNORE INTO products (name, price) VALUES (?, ?)",
            ("Smartphone", 700),
        )

        logging.info("Populated default data.")
        print("\nPopulated default data.")
    except Exception as e:
        logging.error(f"Error populating default data: {e}")
        print(f"\nError populating default data: {e}")


def reset_database():
    """Clear database tables."""
    try:
        db.security_enabled = True  # Reset Security

        # Drop tables
        db.execute("DROP TABLE IF EXISTS users")
        db.execute("DROP TABLE IF EXISTS products")
        db.execute("DROP TABLE IF EXISTS orders")

        # Close connection
        db.close()

        logging.info("Cleared database and closed connection.")
        print("\nCleared database and closed connection.")
    except Exception as e:
        logging.error(f"Error reseting database: {e}")
        print(f"\nError reseting database: {e}")


def is_security_enabled():
    """Return the current security status."""
    return db.security_enabled


def start_flask_api():
    """Start the Flask API server as a subprocess"""
    try:
        # Get the full path of the api.py file
        api_script_path = os.path.join(os.path.dirname(__file__), "api.py")

        # Run the Flask API as a subprocess
        process = subprocess.Popen(["python", api_script_path])

        # Give the server a few seconds to start up
        time.sleep(2)

        logging.info("Flask API server started.")
        print("\nFlask API server started.")

        return process

    except Exception as e:
        logging.error(f"Error starting Flask API server: {e}")
        print(f"\nError starting Flask API server: {e}")


def stop_flask_api(process):
    """Stop the Flask API server process"""
    try:
        if process:
            process.terminate()
            logging.info("Flask API server stopped.")
            print("\nFlask API server stopped.")
    except Exception as e:
        logging.error(f"Error stopping Flask API server: {e}")
        print("\nError stopping Flask API server.")

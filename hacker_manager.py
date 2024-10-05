import requests
from database import Database
from user import User
import logging

db = Database.get_instance()


class HackerManager:
    @staticmethod
    def brute_force_attack(username):
        """Attempt a brute force attack on the given username."""
        try:
            # Block bruce force attack if security is ON
            if db.security_enabled:
                print("\nSecurity is ON. Brute force attack blocked.")
                logging.warning(
                    "Hacker tried brute force attack, but security blocked it."
                )
            else:
                print("\nSecurity is OFF. Attempting brute force attack...")

                common_passwords = [
                    "password123",
                    "test123",
                    "123456",
                    "admin",
                    "password",
                ]

                print(f"Attempting to brute force user: {username}")

                # Check if the user exists
                user_exists_query = (
                    "SELECT username, password FROM users WHERE username = ?"
                )
                user = db.fetchone(user_exists_query, (username,))

                # If the user exists, fetch the hashed password, hash common passwords and check if any of them match.
                if user:
                    hashed_password = user[1]

                    for guess in common_passwords:
                        hashed_guess = User.hash_password(guess)

                        if hashed_password == hashed_guess:
                            logging.warning(f"Hacker brute-forced user '{username}'.")
                            print(
                                f"Brute-force succeeded! User - {username}, Password - {guess}"
                            )
                            return

                logging.warning(
                    f"Hacker tried brute-forcing user '{username}'. Operation failed."
                )
                print("Brute force attack failed.")
        except Exception as e:
            logging.error(f"Error during brute force attack: {e}")
            print(f"\nError during brute force attack: {e}")

    @staticmethod
    def dos_attack():
        """Perform a Denial of Service (DoS) attack simulation."""
        try:
            # Block DoS attack if security is ON
            if db.security_enabled:
                print("\nSecurity is ON. DoS attack blocked.")
                logging.warning("Hacker tried DoS attack, but security blocked it.")
            else:
                print("\nSecurity is OFF. Initiating Denial of Service (DoS) attack...")

                # Simulate a system flood with multiple requests.
                for i in range(1000):
                    view_products_query = "SELECT * FROM products"
                    db.fetchall(view_products_query)
                    print(f"Flooding system with request {i + 1}...")

                logging.warning(f"Hacker performed DOS attack. System overwhelmed.")
                print("DoS attack successful. System overwhelmed.")
        except Exception as e:
            logging.error(f"Error during DoS attack: {e}")
            print(f"\nError during DoS attack: {e}")

    @staticmethod
    def api_injection_attack(username, password):
        """Attempt an API injection attack to create a user."""
        try:
            # Block API injection attack if security is ON
            if db.security_enabled:
                logging.warning(
                    "Hacker tried API injection attack, but security blocked it."
                )
                print("\nSecurity is ON. API injection attack blocked.")
            else:
                print(
                    "\nSecurity is OFF. Attempting API injection attack to create a user..."
                )

                # Send a POST request with malicious input
                api_url = "http://127.0.0.1:5000/create_user"
                malicious_payload = {
                    "username": username,
                    "password": password,
                    "is_admin": True,  # Admin privileges
                }
                response = requests.post(api_url, json=malicious_payload)

                if response.status_code == 201:
                    logging.warning(
                        f"Hacker performed API injection attack. Created user '{username}'."
                    )
                    print(
                        f"API Injection attack succeeded! Created an admin user '{username}' with password '{password}'."
                    )
                else:
                    logging.warning(
                        f"Hacker performed API injection attack. Response -'{response.json()}'."
                    )
                    print(
                        f"API injection failed. Status Code - {response.status_code}, Response - {response.json()}"
                    )
        except Exception as e:
            logging.error(f"Error during API injection attack: {e}")
            print(f"\nError during API injection attack: {e}")

from logger import logging
from user_manager import UserManager
from admin_manager import AdminManager
from hacker_manager import HackerManager
from product_manager import ProductManager
from order_manager import OrderManager
from database import Database
from utils import reset_database, is_security_enabled, start_flask_api, stop_flask_api

db = Database.get_instance()


def user_menu(current_user):
    # Loop to display the user menu until they choose to logout.
    while True:
        print("\nUser Menu")
        print("------------------------")
        print("1. View Products")
        print("2. Place Order")
        print("3. View Orders")
        print("4. Logout")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            ProductManager.view_products(current_user)
        elif choice == "2":
            product_name = input("Enter product name to order: ").strip()
            quantity = input("Enter quantity (Default is 1): ").strip()
            quantity = (
                1
                if not str(quantity).replace(".", "").isnumeric()
                else int(float(quantity))
            )
            confirm = (
                input(
                    f"Are you sure you want to place order for the product '{product_name}' and quantity '{quantity}'? (y/n): "
                )
                .strip()
                .lower()
            )

            OrderManager.place_order(current_user, product_name, quantity, confirm)
        elif choice == "3":
            OrderManager.view_orders_by_user(current_user)
        elif choice == "4":
            logging.info(f"User {current_user} logged out.")
            print("\nLogging out...")

            break
        else:
            print("\nInvalid option, try again.")


def admin_menu(current_user):
    # Loop to display the admin menu until they choose to logout.
    while True:
        print("\nAdmin Menu")
        print("------------------------")
        print("1. View Users")
        print("2. Delete User")
        print("3. View Products")
        print("4. Add Product")
        print("5. Delete Product")
        print("6. View Orders")
        security_status = "ON" if is_security_enabled() else "OFF"
        print(f"7. Toggle Security (Currently {security_status})")
        print("8. View Logs")
        print("9. Logout")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            UserManager.view_users(current_user)
        elif choice == "2":
            username = input("Enter username to delete: ").strip()
            confirm = (
                input(f"Are you sure you want to delete the user '{username}'? (y/n): ")
                .strip()
                .lower()
            )

            UserManager.delete_user(current_user, username, confirm)
        elif choice == "3":
            ProductManager.view_products(current_user)
        elif choice == "4":
            name = input("Enter product name: ").strip()
            price = input("Enter product price (Default is $1.0): ").strip()
            price = 1.0 if not str(price).replace(".", "").isnumeric() else float(price)

            ProductManager.add_or_update_product(current_user, name, price)
        elif choice == "5":
            name = input("Enter the name of the product to delete: ").strip()
            confirm = (
                input(f"Are you sure you want to delete the product '{name}'? (y/n): ")
                .strip()
                .lower()
            )

            ProductManager.delete_product(current_user, name, confirm)
        elif choice == "6":
            OrderManager.view_all_orders(current_user)
        elif choice == "7":
            AdminManager.toggle_security(current_user)
        elif choice == "8":
            AdminManager.view_logs(current_user)
        elif choice == "9":
            logging.info(f"User '{current_user}' logged out.")
            print("\nLogging out...")

            break
        else:
            print("\nInvalid option, try again.")


def hacker_menu():
    # Loop to display hacker menu until they choose to exit.
    while True:
        print("\nHacker Menu")
        print("------------------------")
        print("1. Perform Brute Force Attack")
        print("2. Perform DoS Attack")
        print("3. Perform API Injection Attack")
        print("4. Exit")
        choice = input("\nChoose an option: ")

        if choice == "1":
            username = input("Enter username to brute force: ").strip()

            HackerManager.brute_force_attack(username)
        elif choice == "2":
            HackerManager.dos_attack()
        elif choice == "3":
            username = input("Enter new admin user's username: ").strip()
            password = input("Enter new admin user's password: ").strip()

            HackerManager.api_injection_attack(username, password)
        elif choice == "4":
            break
        else:
            print("\nInvalid option, try again.")


def cli_menu():
    # Start the Flask server to handle API requests.
    flask_process = start_flask_api()

    # Loop to display the main CLI menu until the user chooses to exit.
    while True:
        print("\nWelcome to Online Retailer CLI")
        print("------------------------")
        print("1. Create Account")
        print("2. Login")
        print("3. Hack System")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            is_admin = (
                True
                if input("Is this an admin account? (y/n): ").strip().lower() == "y"
                else False
            )

            UserManager.create_user(username, password, is_admin)
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            current_user = UserManager.login(username, password)

            if not current_user == None:
                if UserManager.check_if_admin(current_user):
                    admin_menu(current_user)
                else:
                    user_menu(current_user)
        elif choice == "3":
            hacker_menu()
        elif choice == "4":
            logging.info("Exited application.")
            print("\nExiting CLI...")

            stop_flask_api(flask_process)  # Stop the Flask server.
            reset_database()
            break
        else:
            print("\nInvalid option, try again.")

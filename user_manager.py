import logging
from user import User
from database import Database

db = Database.get_instance()


class UserManager:
    @staticmethod
    def create_user(username, password, is_admin):
        """Create a new user."""
        try:
            if username and password:

                # Check if the user exists.
                user_exists_query = "SELECT * FROM users WHERE username = ?"
                user = db.fetchone(user_exists_query, (username,))

                # If the user doesn't exist, create a new user.
                if user:
                    logging.error(
                        f"User '{username}' creation failed. User might already exist."
                    )
                    print(
                        f"\nUser '{username}' creation failed. User might already exist."
                    )
                else:
                    hashed_password = User.hash_password(password)
                    insert_user_query = "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)"
                    db.execute(insert_user_query, (username, hashed_password, is_admin))

                    logging.info(f"User '{username}' created.")
                    print(f"\nUser '{username}' created.")
            else:
                logging.error(
                    f"User '{username}' creation failed. Username and password cannot be empty."
                )
                print(
                    f"\nUser '{username}' creation failed. Username and password cannot be empty."
                )
        except Exception as e:
            logging.error(f"An error occurred while creating a user: {e}")
            print("\nAn error occurred while creating a user.")

    @staticmethod
    def login(username, password):
        """
        Logs in a user by checking if the provided username and password match a record in the database.
        """
        try:
            if username and password:
                hashed_password = User.hash_password(password)
                user_exists_query = (
                    "SELECT username, password FROM users WHERE username = ?"
                )
                user = db.fetchone(user_exists_query, (username,))

                # Check if the user exists.
                if user:
                    user_password = user[1]

                    # Check if the password is correct.
                    if hashed_password == user_password:
                        logging.info(f"User '{username}' logged in.")
                        print(f"\nLogin successful! Welcome, {username}.")
                        return username
                    else:
                        logging.error(
                            f"Login failed for user '{username}'. Incorrect password."
                        )
                        print(
                            f"\nLogin failed for user '{username}'. Incorrect password."
                        )
                        return None
                else:
                    logging.error(
                        f"Login failed for user '{username}'. User not found."
                    )
                    print(f"\nLogin failed for user '{username}'. User not found.")
                    return None
            else:
                logging.error(
                    f"User '{username}' creation failed. Username and password cannot be empty."
                )
                print(
                    f"\nUser '{username}' creation failed. Username and password cannot be empty."
                )

            return None
        except Exception as e:
            logging.error(f"An error occurred while logging in: {e}")
            print("\nAn error occurred while logging in.")

    @staticmethod
    def check_if_admin(current_user):
        """Check if the current user has admin privileges."""
        try:
            login_query = "SELECT is_admin FROM users WHERE username = ?"

            # Fetch the admin status of the user and return it.
            user = db.fetchone(login_query, (current_user,))
            is_admin = user[0]

            if is_admin:
                return True
            return False
        except Exception as e:
            logging.error(f"An error occurred while checking admin privilege: {e}")
            print("\nAn error occurred while checking admin privilege.")

    @staticmethod
    def view_users(current_user):
        """
        View all users along with their roles.
        Only admin users can view all users.
        """
        try:
            if UserManager.check_if_admin(current_user):
                view_users_query = "SELECT username, is_admin FROM users"

                # Fetch all users.
                users = db.fetchall(view_users_query)

                if not users:
                    print("\nNo users available.")
                else:
                    for idx, (username, is_admin) in enumerate(users, start=1):
                        role = "Admin" if is_admin else "User"
                        print(f"\nUser {idx}: Username - {username}, Role - {role}")

                logging.info(f"User '{current_user}' requested users.")

                return users
        except Exception as e:
            logging.error(f"An error occurred while viewing users: {e}")
            print("\nAn error occurred while viewing users.")

    @staticmethod
    def delete_user(current_user, username, confirm):
        """Delete the user if current user has admin privileges."""
        try:
            if UserManager.check_if_admin(current_user):
                # Prevent the current user from deleting themselves.
                if current_user == username:
                    logging.error(
                        f"Deletion failed for user '{username}'. Logged-in user."
                    )
                    print(
                        f"\nDeletion failed for user '{username}'. Self-deletion is prohibited."
                    )
                    return

                if confirm == "y":
                    user_exists_query = "SELECT username FROM users WHERE username = ?"

                    # Check if the user exists.
                    user = db.fetchone(user_exists_query, (username,))

                    # Delete the user.
                    if not user:
                        logging.error(
                            f"Deletion failed for user '{username}'. Non-existent user."
                        )
                        print(
                            f"\nDeletion failed for user '{username}'. User does not exist."
                        )
                    else:
                        delete_user_query = "DELETE FROM users WHERE username = ?"
                        db.execute(delete_user_query, (username,))

                        logging.info(
                            f"User '{current_user}' deleted user '{username}'."
                        )
                        print(f"\nUser '{username}' deleted.")
                else:
                    print("\nUser deletion canceled.")
        except Exception as e:
            logging.error(f"An error occurred while deleting a user: {e}")
            print("\nAn error occurred while deleting a user.")

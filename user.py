import hashlib


class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = self.hash_password(password)  # Hash the password and store it.
        self.is_admin = is_admin

    def __str__(self):
        # A human-readable string representation of the user.
        return f"User {self.username}: Role - {"Admin" if self.is_admin else "User"}"

    @staticmethod
    def hash_password(password):
        # Hash the password.
        return hashlib.sha256(password.encode()).hexdigest()

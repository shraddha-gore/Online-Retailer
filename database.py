import sqlite3
import logging


class Database:
    _instance = None

    @staticmethod
    def get_instance():
        # Check if Database instance already exists. If not, create a new instance.
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def __init__(self):
        self.security_enabled = True  # Security ON by default
        self.connection = None
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        # Create a database connection.
        try:
            self.connection = sqlite3.connect("retailer.db", check_same_thread=False)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            logging.error(f"Error creating connection: {e}")
            print(f"\nError creating connection: {e}")

    def close(self):
        # Close the database connection.
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_tables(self):
        # Create new tables
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                               username TEXT PRIMARY KEY,
                               password TEXT,
                               is_admin BOOLEAN)"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS products (
                               name TEXT PRIMARY KEY,
                               price REAL)"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS orders (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               username TEXT,
                               product_name TEXT,
                               quantity INTEGER,
                               total REAL,
                               FOREIGN KEY(username) REFERENCES users(username),
                               FOREIGN KEY(product_name) REFERENCES products(name))"""
        )

        # Commit the changes to the database.
        self.connection.commit()

    def execute(self, query, params=()):
        # Execute a SQL query with the provided parameters and commit the changes to the database.
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query, params=()):
        # Execute a SQL query and fetch all results as a list of tuples.
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        # Execute a SQL query and fetch a single result as a tuple.
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

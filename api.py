from flask import Flask, request, jsonify
from database import Database
from user import User
import logging

app = Flask(__name__)


@app.route("/create_user", methods=["POST"])
def create_user():
    """API endpoint to create a new user."""
    try:
        db = Database.get_instance()
        data = request.get_json()

        # Check if required fields are provided
        if not data or "username" not in data or "password" not in data:
            logging.error(
                f"User creation failed via API. Username and password cannot be empty."
            )
            return jsonify({"error": "Missing required fields."}), 400

        username = str(data["username"]).strip()
        password = str(data["password"]).strip()
        is_admin = True if data.get("is_admin") else False

        # Check if the user already exists
        user_exists_query = "SELECT * FROM users WHERE username = ?"
        existing_user = db.fetchone(user_exists_query, (username,))

        if existing_user:
            logging.error(
                f"User '{username}' creation failed via API. User might already exist."
            )
            return jsonify({"error": "User already exists."}), 409

        # Create a new user
        hashed_password = User.hash_password(password)
        insert_user_query = (
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)"
        )
        db.execute(insert_user_query, (username, hashed_password, is_admin))

        logging.info(f"User '{username}' created via API.")
        return jsonify({"message": "User created.", "user": username}), 201
    except Exception as e:
        logging.error(f"Error creating user via API: {e}")
        return jsonify({"error": "An error occurred while creating a user."}), 500


if __name__ == "__main__":
    app.run()

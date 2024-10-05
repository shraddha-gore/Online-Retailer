import pytest
from user_manager import UserManager
from database import Database
from user import User

db = Database.get_instance()


# This fixture sets up a fresh test database before each test
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    db.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, is_admin INTEGER)"
    )
    yield
    db.execute("DROP TABLE users")


def test_create_user():
    # Arrange
    username = "test_user"
    password = "password123"

    # Act
    UserManager.create_user(username, password, is_admin=False)

    # Assert
    user = db.fetchone("SELECT username FROM users WHERE username = ?", (username,))
    assert user is not None
    assert user[0] == username


def test_create_user_already_exists():
    # Arrange
    username = "existing_user"
    password = "password123"
    hashed_password = User.hash_password(password)

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (username, hashed_password, 0),
    )

    # Act
    UserManager.create_user(username, password, is_admin=False)

    # Assert
    user_count = db.fetchone(
        "SELECT COUNT(*) FROM users WHERE username = ?", (username,)
    )
    assert user_count[0] == 1  # Should still have only one user


def test_login_successful():
    # Arrange
    username = "login_user"
    password = "password123"
    hashed_password = User.hash_password(password)

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (username, hashed_password, 0),
    )

    # Act
    result = UserManager.login(username, password)

    # Assert
    assert result == username


def test_login_failed_incorrect_password():
    # Arrange
    username = "login_user"
    correct_password = "password123"
    wrong_password = "wrong_password"
    hashed_password = User.hash_password(correct_password)

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (username, hashed_password, 0),
    )

    # Act
    result = UserManager.login(username, wrong_password)

    # Assert
    assert result is None


def test_login_failed_non_existent_user():
    # Arrange
    non_existent_username = "non_existent_user"
    password = "password123"

    # Act
    result = UserManager.login(non_existent_username, password)

    # Assert
    assert result is None


def test_view_users():
    # Arrange
    current_user = "admin_user"

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (current_user, "admin_password", 1),
    )
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("regular_user", "user_password", 0),
    )

    # Act
    users = UserManager.view_users(current_user)

    print(users)

    # Assert
    assert users == [
        (current_user, 1),
        ("regular_user", 0),
    ]


def test_delete_user_success():
    # Arrange
    current_user = "admin_user"
    username_to_delete = "user_to_delete"
    confirm = "y"

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (username_to_delete, "password", 0),
    )
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (current_user, "password", 1),
    )

    # Act
    UserManager.delete_user(current_user, username_to_delete, confirm)

    # Assert
    deleted_user = db.fetchone(
        "SELECT * FROM users WHERE username = ?", (username_to_delete,)
    )
    assert deleted_user is None


def test_delete_user_self_deletion():
    # Arrange
    current_user = "admin_user"

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (current_user, "password", 1),
    )

    # Act
    UserManager.delete_user(current_user, current_user, confirm="y")

    # Assert
    deleted_user = db.fetchone(
        "SELECT * FROM users WHERE username = ?", (current_user,)
    )
    assert deleted_user is not None  # The user should not be deleted

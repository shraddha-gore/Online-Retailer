import pytest
from order_manager import OrderManager
from database import Database

db = Database.get_instance()


# This fixture sets up a fresh test database before each test
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    db.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, price REAL)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS orders (username TEXT, product_name TEXT, quantity INTEGER, total REAL)"
    )

    # Adding a sample product for testing
    db.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)", ("Sample Product", 10.0)
    )
    yield
    db.execute("DELETE FROM products")  # Cleanup after each test
    db.execute("DELETE FROM orders")  # Cleanup after each test


def test_place_order(setup_database):
    # Arrange
    current_user = "test_user"
    product_name = "Sample Product"
    quantity = 2
    confirm = "y"

    # Act
    OrderManager.place_order(current_user, product_name, quantity, confirm)

    # Assert
    orders = db.fetchall(
        "SELECT product_name, quantity, total FROM orders WHERE username = ?",
        (current_user,),
    )
    assert len(orders) == 1
    assert orders[0][0] == product_name
    assert orders[0][1] == quantity
    assert orders[0][2] == quantity * 10.0


def test_view_orders_by_user():
    # Arrange
    user_1 = "John"
    user_2 = "David"

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (user_1, "user_password", 0),
    )
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (user_2, "user_password", 0),
    )
    db.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ("Product A", 10.99),
    )
    db.execute(
        "INSERT INTO orders (username, product_name, quantity, total) VALUES (?, ?, ?, ?)",
        (user_1, "Product A", 2, 21.98),
    )
    db.execute(
        "INSERT INTO orders (username, product_name, quantity, total) VALUES (?, ?, ?, ?)",
        (user_1, "Product A", 1, 10.99),
    )
    db.execute(
        "INSERT INTO orders (username, product_name, quantity, total) VALUES (?, ?, ?, ?)",
        (user_2, "Product A", 1, 10.99),
    )

    # Act
    orders = OrderManager.view_orders_by_user(user_1)

    # Assert
    assert orders == [
        ("Product A", 2, 21.98),
        ("Product A", 1, 10.99),
    ]


def test_view_all_orders():
    # Arrange
    current_user = "admin_user"
    regular_user = "test_user"

    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (current_user, "admin_password", 1),
    )
    db.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (regular_user, "user_password", 0),
    )
    db.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ("Product A", 10.99),
    )
    db.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ("Product B", 15.49),
    )
    db.execute(
        "INSERT INTO orders (username, product_name, quantity, total) VALUES (?, ?, ?, ?)",
        (regular_user, "Product A", 1, 10.99),
    )
    db.execute(
        "INSERT INTO orders (username, product_name, quantity, total) VALUES (?, ?, ?, ?)",
        (regular_user, "Product B", 2, 30.98),
    )

    # Act
    orders = OrderManager.view_all_orders(current_user)

    # Assert
    assert orders == [
        (regular_user, "Product A", 1, 10.99),
        (regular_user, "Product B", 2, 30.98),
    ]

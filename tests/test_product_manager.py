import pytest
from product_manager import ProductManager
from database import Database
from user_manager import UserManager

db = Database.get_instance()


# This fixture sets up a fresh test database before each test
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    db.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, price REAL)")
    yield
    db.execute("DELETE FROM products")  # Cleanup after each test


@pytest.fixture
def admin_user():
    # Mock the UserManager's check_if_admin method
    UserManager.check_if_admin = lambda user: True


def test_add_product(admin_user, setup_database):
    # Arrange
    current_user = "admin_user"
    product_name = "New Product"
    product_price = 15.0

    # Act
    ProductManager.add_or_update_product(current_user, product_name, product_price)

    # Assert
    product = db.fetchone("SELECT * FROM products WHERE name = ?", (product_name,))
    assert product is not None
    assert product[0] == product_name
    assert product[1] == product_price


def test_update_product(admin_user, setup_database):
    # Arrange
    current_user = "admin_user"
    product_name = "Existing Product"
    product_price = 10.0

    ProductManager.add_or_update_product(current_user, product_name, product_price)

    updated_price = 20.0

    # Act
    ProductManager.add_or_update_product(current_user, product_name, updated_price)

    # Assert
    product = db.fetchone("SELECT * FROM products WHERE name = ?", (product_name,))
    assert product is not None
    assert product[1] == updated_price


def test_view_products():
    # Arrange
    current_user = "admin_user"

    db.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ("Product A", 10.99),
    )
    db.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        ("Product B", 15.49),
    )

    # Act
    products = ProductManager.view_products(current_user)

    # Assert
    assert products == [
        ("Product A", 10.99),
        ("Product B", 15.49),
    ]


def test_delete_product(admin_user, setup_database):
    # Arrange
    current_user = "admin_user"
    product_name = "Product to Delete"
    product_price = 25.0
    confirm = "y"

    ProductManager.add_or_update_product(current_user, product_name, product_price)

    # Act
    ProductManager.delete_product(current_user, product_name, confirm)

    # Assert
    product = db.fetchone("SELECT * FROM products WHERE name = ?", (product_name,))
    assert product is None  # Product should be deleted

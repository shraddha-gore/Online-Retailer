import logging
from user_manager import UserManager
from database import Database

db = Database.get_instance()


class ProductManager:
    @staticmethod
    def add_or_update_product(current_user, name, price):
        """
        Add a new product or update an existing product's price.
        Only admin users can perform this operation.
        """
        try:
            if UserManager.check_if_admin(current_user):
                if name:
                    product_exists_query = (
                        "SELECT name, price FROM products WHERE name = ?"
                    )
                    product = db.fetchone(product_exists_query, (name,))

                    # Check if the product exists.
                    # If it exists, update its price. Otherwise, add the product.
                    if product:
                        update_product_query = (
                            "UPDATE products SET price = ? WHERE name = ?"
                        )
                        db.execute(update_product_query, (price, name))

                        logging.info(
                            f"User '{current_user}' updated product '{name}' with new price '${price}'."
                        )
                        print(
                            f"\nProduct '{name}' already exists. Updated price is'${price}'."
                        )
                    else:
                        insert_product_query = (
                            "INSERT INTO products (name, price) VALUES (?, ?)"
                        )
                        db.execute(insert_product_query, (name, price))

                        logging.info(
                            f"User '{current_user}' added product '{name}'with price '${price}'."
                        )
                        print(f"\nProduct '{name}' added with price '${price}'.")
                else:
                    logging.error(
                        f"Product update failed. Product name cannot be empty."
                    )
                    print(f"\nProduct name cannot be empty.")
        except Exception as e:
            logging.error(f"An error occurred while updating products: {e}")
            print("\nAn error occurred while updating products.")

    @staticmethod
    def view_products(current_user):
        """View all orders of system."""
        try:
            view_products_query = "SELECT name, price FROM products"

            # Fetch all products.
            products = db.fetchall(view_products_query)

            if not products:
                print("\nNo products available.")
            else:
                for idx, (name, price) in enumerate(products, start=1):
                    print(f"\nProduct {idx}: Name - {name}, Price - ${price:.2f}")

            logging.info(f"User '{current_user}' requested products.")

            return products
        except Exception as e:
            logging.error(f"An error occurred while viewing products: {e}")
            print("\nAn error occurred while viewing products.")

    @staticmethod
    def delete_product(current_user, name, confirm):
        """
        Delete the product.
        Only admin users can delete products.
        """
        try:
            if UserManager.check_if_admin(current_user):
                if name:
                    if confirm == "y":
                        product_exists_query = (
                            "SELECT name FROM products WHERE name = ?"
                        )

                        # Check if the product exists.
                        product = db.fetchone(product_exists_query, (name,))

                        # Delete the product if it exists.
                        if not product:
                            print(f"\nProduct '{name}' not found.")
                        else:
                            delete_product_query = "DELETE FROM products WHERE name = ?"
                            db.execute(delete_product_query, (name,))

                            logging.info(
                                f"User '{current_user}' deleted product '{name}'."
                            )
                            print(f"\nProduct '{name}' deleted.")
                    else:
                        print("\nProduct deletion canceled.")
                else:
                    logging.error(
                        f"Product deletion failed. Product name cannot be empty."
                    )
                    print(f"\nProduct deletion failed. Product name cannot be empty.")
        except Exception as e:
            logging.error(f"An error occurred while deleting a product: {e}")
            print("\nAn error occurred while deleting a product.")

import logging
from database import Database
from user_manager import UserManager

db = Database.get_instance()


class OrderManager:
    @staticmethod
    def place_order(current_user, product_name, quantity, confirm):
        """Place an order for the user."""
        try:
            if not UserManager.check_if_admin(current_user):
                if product_name:
                    if confirm == "y":
                        product_query = (
                            "SELECT name, price FROM products WHERE name = ?"
                        )
                        product = db.fetchone(product_query, (product_name,))

                        # Check if the product exists.
                        if not product:
                            logging.error(
                                f"Order creation failed. Product '{product_name}'not found."
                            )
                            print(f"\nProduct '{product_name}' not found.")
                            return

                        # Calculate total and create an order.
                        product_name, price = product
                        total = price * quantity
                        order_query = "INSERT INTO orders (username, product_name, quantity, total) VALUES (?, ?, ?, ?)"
                        db.execute(
                            order_query,
                            (current_user, product_name, quantity, total),
                        )

                        logging.info(
                            f"User '{current_user}' placed order for {product_name}. Total: ${total}"
                        )
                        print(f"\nOrder placed for {product_name}. Total: ${total}")
                    else:
                        print("\nOrder creation canceled.")
                else:
                    logging.error(
                        f"Order creation failed. Product name cannot be empty."
                    )
                    print(f"\nProduct name cannot be empty.")
        except Exception as e:
            logging.error(f"An error occurred while placing order: {e}")
            print("\nAn error occurred while placing order.")

    @staticmethod
    def view_orders_by_user(current_user):
        """View all orders placed by the current user."""
        try:
            orders_query = """
                SELECT products.name, orders.quantity, orders.total
                FROM orders
                JOIN products ON orders.product_name = products.name
                WHERE orders.username = ?
            """

            # Fetch all orders placed by the current user.
            orders = db.fetchall(orders_query, (current_user,))

            if not orders:
                print("\nNo orders found.")
            else:
                for idx, (product_name, quantity, total) in enumerate(orders, start=1):
                    print(
                        f"\nOrder {idx}: Product - {product_name}, Quantity - {quantity}, Total - ${total:.2f}"
                    )

            logging.info(f"User '{current_user}' requested orders.")

            return orders
        except Exception as e:
            logging.error(f"An error occurred while viewing orders: {e}")
            print("\nAn error occurred while viewing orders.")

    @staticmethod
    def view_all_orders(current_user):
        """View all orders of system if the user has admin privileges."""
        try:
            if UserManager.check_if_admin(current_user):
                orders_query = """
                    SELECT orders.username, products.name, orders.quantity, orders.total
                    FROM orders
                    JOIN products ON orders.product_name = products.name
                """

                # Fetch all orders.
                orders = db.fetchall(orders_query)

                if not orders:
                    print("\nNo orders found.")
                else:
                    for idx, (username, product_name, quantity, total) in enumerate(
                        orders, start=1
                    ):
                        print(
                            f"\nOrder {idx}: User - {username}, Product - {product_name}, Quantity - {quantity}, Total - ${total:.2f}"
                        )

                logging.info(f"User '{current_user}' requested orders.")

                return orders
        except Exception as e:
            logging.error(f"An error occurred while viewing orders: {e}")
            print("\nAn error occurred while viewing orders.")

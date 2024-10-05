class Order:
    def __init__(self, username, product_name, quantity):
        self.username = username
        self.product_name = product_name
        self.quantity = quantity
        self.total = self.calculate_total()  # Calculate and store the total.

    def calculate_total(self):
        # Calculate the order total.
        return self.quantity * self.price_per_item

    def __str__(self):
        # A human-readable string representation of the order.
        return f"Order for {self.username}: Product - {self.product_name}, Quantity - {self.quantity}, Total - ${self.total:.2f}"

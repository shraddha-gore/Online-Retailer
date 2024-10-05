class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        # A human-readable string representation of the product.
        return f"{self.name}: Price - ${self.price:.2f}"

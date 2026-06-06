from werkzeug.exceptions import BadRequest, NotFound


class ProductNotFound(NotFound):
    def __init__(self):
        super().__init__(description="Product not found")


class CustomerNotFound(NotFound):
    def __init__(self):
        super().__init__(description="Customer not found")


class OrderNotFound(NotFound):
    def __init__(self):
        super().__init__(description="Order not found")


class SKUAlreadyExists(BadRequest):
    def __init__(self):
        super().__init__(description="SKU already exists")


class EmailAlreadyExists(BadRequest):
    def __init__(self):
        super().__init__(description="Email already exists")


class InsufficientStock(BadRequest):
    def __init__(self, product_name: str, requested: int, available: int):
        super().__init__(
            description=f"Insufficient stock for {product_name}. Requested: {requested}, Available: {available}"
        )


class NegativeStockError(BadRequest):
    def __init__(self):
        super().__init__(description="Stock quantity cannot be negative")


class InvalidOrderData(BadRequest):
    def __init__(self, detail: str = "Invalid order data"):
        super().__init__(description=detail)

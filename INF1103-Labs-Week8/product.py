class Product:
    """Represents a single product.

    Responsible for storing product information and managing its own state
    (SRP: represent and manage one product, nothing else).
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ----- Getters: controlled, read-only access to private attributes -----
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    # ----- Behaviour -----
    def update_stock(self, quantity: int) -> bool:
        """Sets the stock to a new quantity, validating it first."""
        if quantity < 0:
            print(f"Error: '{quantity}' is not a valid quantity. Stock not updated.")
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self) -> dict:
        """Converts the product into a dictionary for JSON persistence."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Builds a Product from a dictionary (e.g. loaded from inventory.json)."""
        return cls(data["id"], data["name"], data["price"], data["stock"])

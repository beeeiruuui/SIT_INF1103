from can_be_shipped import CanBeShipped
from product import Product


class PhysicalProduct(Product, CanBeShipped):
    SHIPPING_RATE_PER_KG = 2.50

    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        detail = f"Weight: {self.__weight:>6.2f} kg"
        shipping_str = f"${self.calculate_shipping_cost():,.2f}"
        print(f"{'Physical':<{Product.TYPE_WIDTH}} {detail} {shipping_str}")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping to the customer's address."

    def calculate_shipping_cost(self) -> float:
        return self.__weight * self.SHIPPING_RATE_PER_KG

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PhysicalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"], data["weight"])

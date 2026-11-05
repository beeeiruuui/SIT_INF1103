from abc import ABC, abstractmethod


class Product(ABC):
    ID_WIDTH = 6
    NAME_WIDTH = 24
    PRICE_WIDTH = 10
    STOCK_WIDTH = 6
    TYPE_WIDTH = 10

    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> bool:
        if quantity < 0:
            print(f"Error: '{quantity}' is not a valid quantity. Stock not updated.")
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        price_str = f"${self.__price:,.2f}"
        print(
            f"{self.__product_id:<{self.ID_WIDTH}} {self.__name:<{self.NAME_WIDTH}} "
            f"{price_str:>{self.PRICE_WIDTH + 1}} {self.__stock:>{self.STOCK_WIDTH}} ",
            end="",
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        raise NotImplementedError

    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

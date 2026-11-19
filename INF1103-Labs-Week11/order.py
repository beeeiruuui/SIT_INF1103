from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str, discount_strategy: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = (
            discount_strategy if discount_strategy is not None else NoDiscount()
        )

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def remove_order_line(self, index: int) -> bool:
        if 0 <= index < len(self.order_lines):
            del self.order_lines[index]
            return True
        print(f"Error: order line index '{index}' is out of range.")
        return False

    def set_discount(self, discount_strategy: DiscountStrategy) -> None:
        self.discount = discount_strategy

    def calculate_total(self) -> float:
        total = sum(order_line.calculate_subtotal() for order_line in self.order_lines)
        return self.discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder {self.order_id}")
        print("-" * 48)
        for order_line in self.order_lines:
            order_line.display_information()
        print("-" * 48)
        print(f"{'Total:':<40} ${self.calculate_total():,.2f}")

from product import Product


class OrderLine:
    # Evidence of type hints
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity

    def display_information(self) -> None:
        subtotal_str = f"${self.calculate_subtotal():,.2f}"
        print(
            f"{self.product.get_product_id():<{Product.ID_WIDTH}} "
            f"{self.product.get_name():<{Product.NAME_WIDTH}} "
            f"x{self.quantity:<4} {subtotal_str:>12}"
        )

from contextlib import redirect_stdout
from io import StringIO

from product import Product


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def search_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")

        header = (
            f"{'ID':<{Product.ID_WIDTH}} {'Name':<{Product.NAME_WIDTH}} "
            f"{'Price':>{Product.PRICE_WIDTH + 1}} {'Stock':>{Product.STOCK_WIDTH}} "
            f"{'Type':<{Product.TYPE_WIDTH}} Details"
        )

        rows = []
        for product in self.__products:
            buffer = StringIO()
            with redirect_stdout(buffer):
                product.display_information()
            rows.append(buffer.getvalue().rstrip("\n"))

        width = max([len(header)] + [len(row) for row in rows])

        print("=" * width)
        print(header)
        print("-" * width)
        for row in rows:
            print(row)
        print("=" * width)

    def get_all_products(self) -> list[Product]:
        return self.__products

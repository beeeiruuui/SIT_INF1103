from product import Product


class Inventory:
    """Manages a collection of Product objects.

    Responsible for storing, adding, searching and displaying products
    (SRP: manage the collection, not file loading/saving or the menu).
    """

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
        print("-" * 48)
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_all_products(self) -> list[Product]:
        """Exposes the products so the main program can persist them to file."""
        return self.__products

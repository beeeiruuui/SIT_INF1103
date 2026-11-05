from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        detail = f"Download: {self.__download_size:>8.2f} MB"
        print(f"{'Digital':<{Product.TYPE_WIDTH}} {detail} N/A")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally via a download link."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"], data["download_size"])

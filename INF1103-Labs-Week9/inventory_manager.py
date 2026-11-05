import json
from contextlib import redirect_stdout
from io import StringIO

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product

INVENTORY_FILE = "inventory.json"

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def _product_from_dict(data: dict) -> Product:
    product_cls = PRODUCT_TYPES.get(data["type"])
    if product_cls is None:
        raise ValueError(f"Unknown product type: '{data['type']}'")
    return product_cls.from_dict(data)


def load_inventory() -> Inventory:
    inventory = Inventory()

    with open(INVENTORY_FILE, "a+") as f:
        f.seek(0)
        content = f.read()

    data = json.loads(content) if content else []

    if data:
        print(f"{INVENTORY_FILE} found.")
        print("Inventory loaded successfully.")
    else:
        print(f"{INVENTORY_FILE} not found.")
        print("Starting with empty inventory.")

    for item in data:
        inventory.add_product(_product_from_dict(item))

    return inventory


def save_inventory(inventory: Inventory) -> None:
    print("\nSaving inventory...")
    data = [product.to_dict() for product in inventory.get_all_products()]
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Inventory saved successfully to {INVENTORY_FILE}.")


def exit_program(inventory: Inventory) -> None:
    print("\nSaving inventory before exit...")
    save_inventory(inventory)
    print("\nThank you for using Inventory Management System.")
    print("Program terminated.")


def _read_common_fields() -> tuple[str, str, float, int] | None:
    product_id = input("Product ID: ")
    name = input("Product Name: ")

    price_entry = input("Price: ")
    try:
        price = float(price_entry)
    except ValueError:
        print(f"Error: '{price_entry}' is not a valid price. Product not added.")
        return None

    stock_entry = input("Stock Quantity: ")
    if not stock_entry.isdigit():
        print(f"Error: '{stock_entry}' is not a valid quantity. Product not added.")
        return None

    return product_id, name, price, int(stock_entry)


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Select product type (1-2): ")

    if product_type not in ("1", "2"):
        print(f"Error: '{product_type}' is not a valid product type. Product not added.")
        return

    common = _read_common_fields()
    if common is None:
        return
    product_id, name, price, stock = common

    if product_type == "1":
        weight_entry = input("Weight (kg): ")
        try:
            weight = float(weight_entry)
        except ValueError:
            print(f"Error: '{weight_entry}' is not a valid weight. Product not added.")
            return
        product: Product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        size_entry = input("Download Size (MB): ")
        try:
            download_size = float(size_entry)
        except ValueError:
            print(f"Error: '{size_entry}' is not a valid download size. Product not added.")
            return
        product = DigitalProduct(product_id, name, price, stock, download_size)

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    stock_entry = input("\nNew Stock Quantity: ")
    if not stock_entry.isdigit():
        print(f"Error: '{stock_entry}' is not a valid quantity. Stock not updated.")
        return

    product.update_stock(int(stock_entry))
    print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")

    buffer = StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    row = buffer.getvalue().rstrip("\n")

    indent = " " * (Product.ID_WIDTH + 1)
    fulfilment_line = f"{indent}Fulfilment: {product.get_fulfilment_info()}"
    width = max(len(row), len(fulfilment_line))

    print("=" * width)
    print(row)
    print(fulfilment_line)
    print("=" * width)


def print_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 24)


def main() -> None:
    print("=" * 48)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 48)

    inventory = load_inventory()

    while True:
        print_menu()
        option = input("\nEnter option: ")

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            exit_program(inventory)
            break
        else:
            print(f"\nInvalid option '{option}'. Please try again.")


if __name__ == "__main__":
    main()

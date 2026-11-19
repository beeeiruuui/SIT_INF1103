import csv
import json
from contextlib import redirect_stdout
from io import StringIO

from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

INVENTORY_FILE = "inventory.json"


def load_inventory() -> Inventory:
    inventory = Inventory()

    with open(INVENTORY_FILE, "a+", encoding="utf-8") as file:
        file.seek(0)
        content = file.read()

    data = json.loads(content) if content else []

    if data:
        print(f"{INVENTORY_FILE} found.")
        print("Inventory loaded successfully.")
    else:
        print(f"{INVENTORY_FILE} not found.")
        print("Starting with empty inventory.")

    for item in data:
        product_type = item["type"]
        supplier = Supplier.from_dict(item["supplier"])
        product = ProductFactory.create(
            product_type,
            item["id"],
            item["name"],
            item["price"],
            item["stock"],
            supplier,
            weight=item.get("weight", 0.0),
            download_size=item.get("download_size", 0.0),
        )
        inventory.add_product(product)

    return inventory


def save_inventory(inventory: Inventory) -> None:
    print("\nSaving inventory...")
    data = [product.to_dict() for product in inventory.get_all_products()]
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved successfully to {INVENTORY_FILE}.")


def exit_program(inventory: Inventory) -> None:
    print("\nSaving inventory before exit...")
    save_inventory(inventory)
    print("\nThank you for using Inventory Management System.")
    print("Program terminated.")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)
            for row_number, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Expected 5 columns.")
                    product = ProductFactory.create(
                        row[0].strip(),
                        row[1].strip(),
                        row[2].strip(),
                        float(row[3].strip()),
                        int(row[4].strip()),
                        supplier,
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def _read_common_fields() -> tuple[str, str, float, int] | None:
    product_id = input("Product ID: ")
    name = input("Product Name: ")
    price = get_positive_float("Price: ")

    stock_entry = input("Stock Quantity: ")
    if not stock_entry.isdigit():
        print(f"Error: '{stock_entry}' is not a valid quantity. Product not added.")
        return None

    return product_id, name, price, int(stock_entry)


def _read_supplier() -> Supplier:
    print("\nSupplier Details")
    supplier_id = input("Supplier ID: ")
    name = input("Supplier Name: ")
    contact_email = input("Supplier Contact Email: ")
    return Supplier(supplier_id, name, contact_email)


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_choice = input("Select product type (1-2): ")

    product_types = {"1": "physical", "2": "digital"}
    product_type = product_types.get(product_choice)
    if product_type is None:
        print(f"Error: '{product_choice}' is not a valid product type. Product not added.")
        return

    common = _read_common_fields()
    if common is None:
        return
    product_id, name, price, stock = common
    supplier = _read_supplier()

    product_details: dict[str, float] = {}
    if product_type == "physical":
        weight_entry = input("Weight (kg): ")
        try:
            product_details["weight"] = float(weight_entry)
        except ValueError:
            print(f"Error: '{weight_entry}' is not a valid weight. Product not added.")
            return
    else:
        size_entry = input("Download Size (MB): ")
        try:
            product_details["download_size"] = float(size_entry)
        except ValueError:
            print(f"Error: '{size_entry}' is not a valid download size. Product not added.")
            return

    try:
        product = ProductFactory.create(
            product_type, product_id, name, price, stock, supplier, **product_details
        )
    except ValueError as error:
        print(f"Error: {error} Product not added.")
        return

    inventory.add_product(product)
    print("\nProduct added successfully!")


def load_products_from_file(inventory: Inventory) -> None:
    print("\nLoad Products from CSV")
    path = input("CSV file path (blank for products.csv): ").strip() or "products.csv"
    supplier = _read_supplier()
    load_products(path, inventory, supplier)


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ")
    product = inventory.find_product(product_id)

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
    product = inventory.find_product(product_id)

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
    supplier_line = (
        f"{indent}Supplier: {product.supplier.get_name()} "
        f"({product.supplier.get_contact_email()})"
    )
    width = max(len(row), len(fulfilment_line), len(supplier_line))

    print("=" * width)
    print(row)
    print(fulfilment_line)
    print(supplier_line)
    print("=" * width)


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product from Inventory")
    product_id = input("Enter Product ID: ")

    if inventory.find_product(product_id) is None:
        print("\nProduct not found.")
        return

    inventory.remove_product(product_id)
    print("\nProduct removed from inventory (the Product object itself still exists).")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def create_order(inventory: Inventory, orders: list[Order]) -> None:
    print("\nCreate New Order")
    order_id = input("Order ID: ")
    order = Order(order_id)

    while True:
        product_id = input("\nEnter Product ID to add (blank to finish): ")
        if not product_id:
            break

        product = inventory.find_product(product_id)
        if product is None:
            print("\nProduct not found in inventory.")
            continue

        quantity_entry = input("Quantity: ")
        if not quantity_entry.isdigit() or int(quantity_entry) <= 0:
            print(f"Error: '{quantity_entry}' is not a valid quantity. Line not added.")
            continue

        order.add_order_line(product, int(quantity_entry))
        print("Order line added.")

    orders.append(order)
    order.display_order()
    print("\nOrder created successfully!")


def display_orders(orders: list[Order]) -> None:
    if not orders:
        print("\nNo orders have been created yet.")
        return
    for order in orders:
        order.display_order()


def print_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product from Inventory")
    print("6. Create Order")
    print("7. Display Orders")
    print("8. Save Inventory")
    print("9. Load Products from CSV")
    print("10. Exit")
    print("-" * 24)


def main() -> None:
    print("=" * 48)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 48)

    inventory = load_inventory()
    orders: list[Order] = []

    while True:
        print_menu()
        option = input("\nEnter option: ")

        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            remove_product(inventory)
        elif option == "6":
            create_order(inventory, orders)
        elif option == "7":
            display_orders(orders)
        elif option == "8":
            save_inventory(inventory)
        elif option == "9":
            load_products_from_file(inventory)
        elif option == "10":
            exit_program(inventory)
            break
        else:
            print(f"\nInvalid option '{option}'. Please try again.")


if __name__ == "__main__":
    main()

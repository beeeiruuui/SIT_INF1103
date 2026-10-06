import json

Inventory_File = "INF1103-Labs-Week5/inventory.json"

def _read_inventory():
    with open(Inventory_File, "a+") as f:
        f.seek(0)
        content = f.read()
    return json.loads(content) if content else []


def load_inventory():
    inventory = _read_inventory()

    if inventory:
        print(f"{Inventory_File} found.")
        print("Inventory loaded successfully.")
    else:
        print(f"{Inventory_File} not found.")
        print("Starting with empty inventory.")

    return inventory

def _write_inventory(inventory):
    products = []
    for product in inventory:
        keys = ",\n".join(f'"{key}": {json.dumps(value)}' for key, value in product.items())
        products.append("    {\n" + keys + "\n    }")
    with open(Inventory_File, "w") as f:
        f.write("[\n" + ",\n".join(products) + "\n]")


def save_inventory(inventory):
    print("\nSaving inventory...")
    with open(Inventory_File, "w") as f:
        json.dump(inventory, f, indent=4)
    print(f"Inventory saved successfully to {Inventory_File}.")


def exit_program(inventory):
    print("\nSaving inventory before exit...")
    save_inventory(inventory)
    print("\nThank you for using Inventory Management System.")
    print("Program terminated.")


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ")
    name = input("Product Name: ")

    price_entry = input("Price: ")
    try:
        price = float(price_entry)
    except ValueError:
        print(f"Error: '{price_entry}' is not a valid price. Product not added.")
        return

    stock_entry = input("Stock Quantity: ")
    if not stock_entry.isdigit():
        print(f"Error: '{stock_entry}' is not a valid quantity. Product not added.")
        return None

    product = {"id": product_id, "name": name, "price": price, "stock": int(stock_entry)}
    inventory.append(product)
    print("\nProduct added successfully!")
    return product


def find_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ")
    product = find_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    stock_entry = input("\nNew Stock Quantity: ")
    if not stock_entry.isdigit():
        print(f"Error: '{stock_entry}' is not a valid quantity. Stock not updated.")
        return

    product["stock"] = int(stock_entry)
    print("\nStock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")
    product = find_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    for product in inventory:
        print(
            f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
        )
    print("-" * 48)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("-" * 24)


def main():
    print("=" * 48)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 48)

    inventory = load_inventory()

    while True:
        print_menu()
        option = input("\nEnter option: ")

        if option == "1":
            inventory = _read_inventory()
            display_all(inventory)
        elif option == "2":
            inventory = _read_inventory()
            new_product = add_product(inventory)
            if new_product is not None:
                _write_inventory(inventory)
        elif option == "3":
            inventory = _read_inventory()
            update_stock(inventory)
            _write_inventory(inventory)
        elif option == "4":
            inventory = _read_inventory()
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

INVENTORY_FILE = "inventory.txt"


def load_inventory():
    inventory = []
    with open(INVENTORY_FILE, "a+") as f:
        f.seek(0)
        for line in f.readlines():
            order_id, name, qty = line.split(",")
            inventory.append((int(order_id), name, int(qty)))
    return inventory


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as f:
        for order_id, name, qty in inventory:
            f.write(f"{order_id}, {name}, {qty}\n")


def get_new_order(next_id):
    name = input("\nEnter Product Name: ")

    if name.lower() == "quit":
        return "quit"

    qty_entry = input("Enter Quantity: ")

    if not qty_entry.isdigit():
        print(f"Error: '{qty_entry}' is not a valid number. Entry rejected.")
        return None

    quantity = int(qty_entry)

    if quantity < 0:
        print(f"Error: negative quantity '{quantity}' is not allowed. Entry rejected.")
        return None

    return next_id, name, quantity


def main():
    inventory = load_inventory()

    print("Current Orders:\n")
    for order_id, name, qty in inventory:
        print(f"{order_id}, {name}, {qty}")

    while True:
        next_id = (max(order_id for order_id, _, _ in inventory) + 1) if inventory else 1001
        result = get_new_order(next_id)

        if result == "quit":
            save_inventory(inventory)
            print(f"\nOrder successfully saved to {INVENTORY_FILE}")
            break

        if result is None:
            continue

        inventory.append(result)
        order_id, name, qty = result
        print(f"\nNew Order Added:\n{order_id}, {name}, {qty}")

        save_inventory(inventory)
        print(f"\nOrder successfully saved to {INVENTORY_FILE}")


if __name__ == "__main__":
    main()

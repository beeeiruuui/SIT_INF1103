def get_valid_input():
    """Prompt for a stock quantity. Returns an int, or 'quit' to signal exit."""
    entry = input("Enter stock quantity (or 'quit' to finish): ")

    if entry.lower() == "quit":
        return "quit"

    if not entry.isdigit():
        print(f"Error: '{entry}' is not a valid number. Entry rejected.")
        return None

    quantity = int(entry)

    if quantity < 0:
        print(f"Error: negative quantity '{quantity}' is not allowed. Entry rejected.")
        return None

    return quantity


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_units = 0
    processed_count = 0
    failed_attempts = 0

    while True:
        entry = get_valid_input()

        if entry == "quit":
            break

        if entry is None:
            failed_attempts += 1
            continue

        total_units = process_delivery(total_units, entry)
        tax = calculate_tax(entry)
        processed_count += 1
        print(f"Delivery of {entry} units recorded. Tax for this delivery: {tax:.2f}")

        if total_units > 500:
            print(f"ALERT: Overstock detected! Total inventory ({total_units}) exceeds 500 units.")
            break

    generate_report(total_units, failed_attempts)


if __name__ == "__main__":
    main()

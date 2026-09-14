total_units = 0
processed_count = 0
failed_count = 0

while True:
    entry = input("Enter stock quantity (or 'quit' to finish): ")

    if entry.lower() == "quit":
        break

    if not entry.isdigit():
        print(f"Error: '{entry}' is not a valid number. Entry rejected.")
        failed_count += 1
        continue

    quantity = int(entry)

    if quantity < 0:
        print(f"Error: negative quantity '{quantity}' is not allowed. Entry rejected.")
        failed_count += 1
        continue
    else:
        total_units += quantity
        processed_count += 1

    if total_units > 500:
        print(f"ALERT: Overstock detected! Total inventory ({total_units}) exceeds 500 units.")
        break

print(f"Total Units Processed: {total_units}")
print(f"Number of Failed/Rejected Entries: {failed_count}")

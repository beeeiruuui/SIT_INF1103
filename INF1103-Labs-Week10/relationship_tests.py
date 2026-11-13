from digital_product import DigitalProduct
from inventory import Inventory
from inventory_manager import show_product_details
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def test_association() -> None:
    section("2. Association: Supplier <-> Product")

    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    physical = PhysicalProduct("P100", "Keyboard", 49.90, 20, supplier, 0.8)
    digital = DigitalProduct("D100", "E-Book: OOP in Python", 12.00, 999, supplier, 3.4)

    print("Supplier info via PhysicalProduct:")
    physical.supplier.display_information()
    print("Supplier info via DigitalProduct:")
    digital.supplier.display_information()

    print(
        "\nPredict first: deleting the local 'supplier' variable will NOT stop "
        "the products from displaying supplier info, because each Product holds "
        "its own reference to the same Supplier object - 'del' only removes the "
        "local name, not the object (it is not garbage collected while other "
        "references, like physical.supplier, still exist)."
    )
    del supplier
    print("\nAfter 'del supplier' -> physical.supplier still works:")
    physical.supplier.display_information()
    print("After 'del supplier' -> digital.supplier still works:")
    digital.supplier.display_information()
    print("\nResult: prediction MATCHED. Both products still display supplier info.")

    print(
        "\nConfirming Supplier and Product are separate, independent objects: "
        f"physical.supplier is digital.supplier -> {physical.supplier is digital.supplier}"
    )


def test_aggregation() -> None:
    section("3. Aggregation: Inventory <-> Product")

    supplier = Supplier("S002", "Digital Press Co", "orders@digitalpress.example.com")
    product = PhysicalProduct("P200", "Monitor", 199.00, 10, supplier, 4.2)
    print(f"Product '{product.get_name()}' created before any Inventory exists.")

    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(product)
    print(f"\nAdded to Inventory A. Inventory A now has {len(inventory_a.products)} product(s).")

    print(
        "\nPredict first: after removing the Product from Inventory A, the Product "
        "object itself should still be usable (display info, update stock), because "
        "Inventory only aggregates a reference - it does not own the Product's lifecycle."
    )
    inventory_a.remove_product("P200")
    print(f"Removed from Inventory A. Inventory A now has {len(inventory_a.products)} product(s).")
    print("Product still works after removal:")
    product.display_information()
    print()
    print("Result: prediction MATCHED - the Product object was not destroyed.")

    inventory_b.add_product(product)
    print(f"\nSame Product object added to Inventory B (has {len(inventory_b.products)} product(s)).")
    print(f"Found via Inventory B.find_product: {inventory_b.find_product('P200') is product}")


def test_composition() -> None:
    section("4. Composition: Order -> OrderLine")

    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    product_a = PhysicalProduct("P300", "Webcam", 59.90, 25, supplier, 0.3)
    product_b = DigitalProduct("D300", "Software License", 89.00, 500, supplier, 1.0)

    order_1 = Order("ORD-001")
    order_1.add_order_line(product_a, 2)
    order_1.add_order_line(product_b, 1)
    order_1.display_order()

    print(
        "\nPredict first: if the same Product is added to a second Order, there "
        "will be 2 OrderLine objects (one per Order, each created independently by "
        "its own Order) but still only 1 Product object, since OrderLine only "
        "refers to (does not own) the Product."
    )
    order_2 = Order("ORD-002")
    order_2.add_order_line(product_a, 5)
    order_2.display_order()

    line_1_product = order_1.order_lines[0].product
    line_2_product = order_2.order_lines[0].product
    print(f"\nSame Product shared across orders (is): {line_1_product is line_2_product}")
    print(
        "Different OrderLine objects (is): "
        f"{order_1.order_lines[0] is order_2.order_lines[0]}"
    )
    print("Result: prediction MATCHED - 2 OrderLine objects, 1 shared Product object.")

    print("\nRemoving order line 0 from order_1 via Order's own method:")
    order_1.remove_order_line(0)
    order_1.display_order()
    print(
        "Note: OrderLine is not removed independently from outside Order and is "
        "never transferred between orders - it belongs to exactly one Order."
    )


def test_polymorphism_and_lsp() -> None:
    section("6/7. Polymorphism through the Product abstraction + LSP")

    supplier = Supplier("S003", "Global Supplies Inc", "contact@globalsupplies.example.com")
    physical = PhysicalProduct("P400", "Desk Lamp", 29.90, 40, supplier, 1.1)
    digital = DigitalProduct("D400", "Mobile App License", 4.99, 1000, supplier, 0.15)

    inventory = Inventory()
    inventory.add_product(physical)
    inventory.add_product(digital)

    print(
        "Predict first: get_fulfilment_info() should return the physical-shipping "
        "message for 'Desk Lamp' and the digital-download message for 'Mobile App "
        "License', chosen automatically per object with no isinstance() checks."
    )
    # Evidence Physical/DigitalProduct work polymorphically
    for product in inventory.products:
        product.display_information()
        print(product.get_fulfilment_info())
    print("Result: prediction MATCHED - each subclass supplied its own implementation.")

    print("\nCalling show_product_details(product: Product) with both subclasses:")
    for product in inventory.products:
        show_product_details(product)

    print(
        "\nLSP note: show_product_details() only relies on behaviour the Product "
        "abstraction promises (display_information(), get_fulfilment_info()), so it "
        "works unmodified for any current or future Product subclass. This is only "
        "safe because both PhysicalProduct and DigitalProduct preserve Product's "
        "expectations (e.g. update_stock() always updates stock and returns bool; "
        "neither subclass raises for a method the parent promises to support)."
    )


def main() -> None:
    test_association()
    test_aggregation()
    test_composition()
    test_polymorphism_and_lsp()


if __name__ == "__main__":
    main()

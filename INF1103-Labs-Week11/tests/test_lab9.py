import csv
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from digital_product import DigitalProduct  # noqa: E402
from discount_strategy import (  # noqa: E402
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount,
)
from inventory import Inventory  # noqa: E402
from inventory_manager import get_positive_float, load_products  # noqa: E402
from order import Order  # noqa: E402
from order_line import OrderLine  # noqa: E402
from physical_product import PhysicalProduct  # noqa: E402
from product_factory import ProductFactory  # noqa: E402
from supplier import Supplier  # noqa: E402


class Lab9Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Lab Supplier", "lab@example.com")
        self.product = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 25.0, 10, self.supplier, weight=1.0
        )

    def test_order_uses_replaceable_discount_strategy(self) -> None:
        order = Order("ORD-001")
        order.add_order_line(self.product, 10)

        self.assertEqual(order.calculate_total(), 250.0)

        order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

        order.set_discount(StudentDiscount())
        self.assertEqual(order.calculate_total(), 237.5)

    def test_order_defaults_to_no_discount(self) -> None:
        order = Order("ORD-002")
        order.add_order_line(self.product, 10)

        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_order_accepts_strategy_when_created(self) -> None:
        order = Order("ORD-003", BulkDiscount(200, 20))
        order.add_order_line(self.product, 10)

        self.assertEqual(order.calculate_total(), 230.0)

    def test_bulk_discount_only_applies_at_or_above_threshold(self) -> None:
        strategy = BulkDiscount(200, 20)

        self.assertEqual(strategy.apply(199.99), 199.99)
        self.assertEqual(strategy.apply(200.0), 180.0)

    def test_new_strategy_works_without_changing_order(self) -> None:
        class HalfPriceDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        order = Order("ORD-004")
        order.add_order_line(self.product, 10)
        order.set_discount(HalfPriceDiscount())

        self.assertEqual(order.calculate_total(), 125.0)

    def test_order_contains_no_discount_branching(self) -> None:
        source = (PROJECT_DIR / "order.py").read_text(encoding="utf-8")

        self.assertNotIn("elif", source)
        self.assertNotIn("discount_type", source)

    def test_no_discount_leaves_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_order_line_rejects_non_positive_quantity(self) -> None:
        with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero"):
            OrderLine(self.product, 0)
        with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero"):
            OrderLine(self.product, -3)

    def test_application_creates_products_through_factory_only(self) -> None:
        source = (PROJECT_DIR / "inventory_manager.py").read_text(encoding="utf-8")

        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)
        self.assertIn("ProductFactory.create(", source)

    def test_product_factory_creates_both_product_types(self) -> None:
        physical = ProductFactory.create(
            "physical", "P002", "Chair", 50.0, 3, self.supplier, weight=4.0
        )
        digital = ProductFactory.create("digital", "D001", "Editor", 20.0, 5, self.supplier)

        self.assertIsInstance(physical, PhysicalProduct)
        self.assertEqual(physical.get_weight(), 4.0)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(digital.get_download_size(), 0.0)

    def test_factory_rejects_unknown_product_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown product type"):
            ProductFactory.create("service", "S001", "Install", 30.0, 1, self.supplier)

    def test_product_validation_rejects_invalid_price_and_stock(self) -> None:
        with self.assertRaisesRegex(ValueError, "Price must be greater than zero"):
            ProductFactory.create("physical", "P002", "Chair", 0.0, 3, self.supplier)
        with self.assertRaisesRegex(ValueError, "Price must be greater than zero"):
            ProductFactory.create("digital", "D002", "Editor", -5.0, 3, self.supplier)
        with self.assertRaisesRegex(ValueError, "Stock quantity cannot be negative"):
            ProductFactory.create("digital", "D001", "Editor", 20.0, -1, self.supplier)

    def test_positive_float_retries_invalid_and_non_positive_values(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(output):
                value = get_positive_float("Price: ")

        self.assertEqual(value, 12.5)
        self.assertIn("Please enter a valid number", output.getvalue())
        self.assertIn("Please enter a number greater than zero", output.getvalue())

    def test_csv_loader_loads_valid_rows_and_skips_invalid_rows(self) -> None:
        inventory = Inventory()
        csv_content = [
            ["product_type", "product_id", "name", "price", "stock_quantity"],
            ["physical", "P001", "Desk Lamp", "25.00", "10"],
            ["digital", "D001", "Photo Editor", "49.90", "100"],
            ["physical", "P002", "Office Chair", "abc", "3"],
            ["service", "S001", "Installation", "30.00", "5"],
        ]
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "products.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as file:
                csv.writer(file).writerows(csv_content)

            with redirect_stdout(output):
                load_products(str(csv_path), inventory, self.supplier)

        self.assertEqual(len(inventory.get_all_products()), 2)
        self.assertIn("Skipping row 4", output.getvalue())
        self.assertIn("Skipping row 5", output.getvalue())
        self.assertIn("2 products loaded.", output.getvalue())
        self.assertTrue(output.getvalue().rstrip().endswith("Load attempt finished."))

    def test_provided_products_csv_loads_three_valid_rows(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(str(PROJECT_DIR / "products.csv"), inventory, self.supplier)

        loaded_ids = [product.get_product_id() for product in inventory.get_all_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertIn("3 products loaded.", output.getvalue())

    def test_csv_loader_handles_missing_file_and_always_finishes(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            missing_path = str(Path(directory) / "missing.csv")
            with redirect_stdout(output):
                load_products(missing_path, inventory, self.supplier)

        self.assertIn("Products file not found", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())
        self.assertEqual(inventory.get_all_products(), [])


if __name__ == "__main__":
    unittest.main()

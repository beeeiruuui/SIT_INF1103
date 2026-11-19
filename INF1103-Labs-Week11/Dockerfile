FROM python:3.11-slim
WORKDIR /app
COPY supplier.py .
COPY product.py .
COPY can_be_shipped.py .
COPY physical_product.py .
COPY digital_product.py .
COPY inventory.py .
COPY discount_strategy.py .
COPY order_line.py .
COPY order.py .
COPY product_factory.py .
COPY inventory_manager.py .
COPY inventory.json .
COPY products.csv .
COPY tests ./tests
CMD ["python", "inventory_manager.py"]

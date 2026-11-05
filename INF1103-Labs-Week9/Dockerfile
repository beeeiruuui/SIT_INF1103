FROM python:3.11-slim
WORKDIR /app
COPY product.py .
COPY can_be_shipped.py .
COPY physical_product.py .
COPY digital_product.py .
COPY inventory.py .
COPY inventory_manager.py .
COPY inventory.json .
CMD ["python", "inventory_manager.py"]

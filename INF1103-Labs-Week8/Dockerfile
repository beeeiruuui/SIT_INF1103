FROM python:3.11-slim
WORKDIR /app
COPY product.py .
COPY inventory.py .
COPY inventory_manager.py .
COPY inventory.json .
CMD ["python", "inventory_manager.py"]

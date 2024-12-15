FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service files
COPY . /app

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. product.proto

EXPOSE 3002

CMD ["python", "server.py"]
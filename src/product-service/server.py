import grpc
from concurrent import futures
import product_pb2
import product_pb2_grpc
import os
import uuid
from typing import Dict, List

class ProductServicer(product_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products: Dict[str, product_pb2.Product] = {}

    def GetProducts(self, request, context):
        print('Tupoooooooooo')
        return product_pb2.ProductList(products=list(self.products.values()))

    def GetProduct(self, request, context):
        if request.id not in self.products:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')
            return product_pb2.Product()
        return self.products[request.id]

    def CreateProduct(self, request, context):
        product_id = str(uuid.uuid4())
        product = product_pb2.Product(
            id=product_id,
            name=request.name,
            description=request.description,
            price=request.price,
            image_url=request.image_url,
            available=request.available
        )
        self.products[product_id] = product
        return product

    def UpdateProduct(self, request, context):
        if request.id not in self.products:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')
            return product_pb2.Product()
        self.products[request.id] = request
        return request

    def DeleteProduct(self, request, context):
        if request.id not in self.products:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Product not found')
            return product_pb2.Empty()
        del self.products[request.id]
        return product_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        ProductServicer(), server
    )
    port = os.getenv('PORT', '3002')
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

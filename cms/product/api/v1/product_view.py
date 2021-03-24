from django.db import transaction
from product.serializers import ProductSerializer
from product.services.product_service import ProductService
from rest_framework import generics, status
from utils.responses import success_response

class ProductView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    # Get all entities
    def get(self, request, entity_id):
        product_service = ProductService(data=request)
        result = product_service.get_all(entity_id=entity_id)
        if result:
            return success_response(message="Product data retrieved successfully.", data=result)
        else:
            return success_response(message="Product data not found.")

    # Create entity
    @transaction.atomic
    def post(self, request, entity_id):
        product_service = ProductService(data=request.data)
        response = product_service.create(entity_id=entity_id)
        if response:
            return success_response(message='Product added successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Product creation failure.')


class ProductDetailView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    # Get entity details by id
    def get(self, request, entity_id, id):
        product_service = ProductService({})
        result = product_service.get(id, entity_id)
        if result:
            return success_response(message="Product data retrieved successfully.", data=result)
        else:
            return success_response(message="Product data not found.")

    # Update entity details
    @transaction.atomic
    def put(self, request, entity_id, id):
        product_service = ProductService(data=request.data)
        if product_service.update(id, entity_id):
            return success_response(message='Product updated successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Cannot update vendor.')

    # Update status to inactive of entity
    @transaction.atomic
    def delete(self, request, entity_id, id):

        product_service = ProductService({})
        if product_service.delete(id=id, entity_id=entity_id):
            return success_response(message="Product removed successfully")
        else:
            return success_response(message="Cannot remove entity")

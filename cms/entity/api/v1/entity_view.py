from django.db import transaction
from entity.serializers import EntitySerializer
from entity.services.entity_service import EntityService
from rest_framework import generics, status
from utils.responses import success_response

class EntityView(generics.GenericAPIView):
    serializer_class = EntitySerializer

    # Get all entities
    def get(self, request, company_id):
        entity_service = EntityService(data=request)
        result = entity_service.get_all(company_id=company_id)
        if result:
            return success_response(message="Entity data retrieved successfully.", data=result)
        else:
            return success_response(message="Entity data not found.")

    # Create entity
    @transaction.atomic
    def post(self, request, company_id):
        entity_service = EntityService(data=request.data)
        response = entity_service.create(company_id=company_id)
        if response:
            return success_response(message='Entity added successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Entity creation failure.')


class EntityDetailView(generics.GenericAPIView):
    serializer_class = EntitySerializer

    # Get entity details by id
    def get(self, request, company_id, id):
        entity_service = EntityService({})
        result = entity_service.get(id, company_id)
        if result:
            return success_response(message="Entity data retrieved successfully.", data=result)
        else:
            return success_response(message="Entity data not found.")

    # Update entity details
    @transaction.atomic
    def put(self, request, company_id, id):
        entity_service = EntityService(data=request.data)
        if entity_service.update(id, company_id):
            return success_response(message='Entity updated successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Cannot update vendor.')

    # Update status to inactive of entity
    @transaction.atomic
    def delete(self, request, company_id, id):
        # Update entity status to inactive
        entity_service = EntityService(data=request.data)
        if entity_service.delete(id=id, company_id=company_id):
            return success_response(message="Entity removed successfully")
        else:
            return success_response(message="Cannot remove entity")

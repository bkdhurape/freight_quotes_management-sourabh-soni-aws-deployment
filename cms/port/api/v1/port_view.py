from django.db import transaction
from port.serializers import PortSerializer
from port.services.port_service import PortService
from rest_framework import generics, status
from utils.responses import success_response

class PortView(generics.GenericAPIView):
    serializer_class = PortSerializer

    # Get all entities
    def get(self, request):
        port_service = PortService(data=request)
        result = port_service.get_all()
        if result:
            return success_response(message="Port data retrieved successfully.", data=result)
        else:
            return success_response(message="Port data not found.")

    # Create port
    @transaction.atomic
    def post(self, request):
        port_service = PortService(data=request.data)
        response = port_service.create()
        if response:
            return success_response(message='Port added successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Port creation failure.')


class PortDetailView(generics.GenericAPIView):
    serializer_class = PortSerializer

    # Get port details by id
    def get(self, request, id):
        port_service = PortService({})
        result = port_service.get(id)
        if result:
            return success_response(message="Port data retrieved successfully.", data=result)
        else:
            return success_response(message="Port data not found.")

    # Update port details
    @transaction.atomic
    def put(self, request, id):
        port_service = PortService(data=request.data)
        if port_service.update(id):
            return success_response(message='Port updated successfully.')
        else:
            return success_response(status_code=status.HTTP_400_BAD_REQUEST, status='failure',
                                   message='Cannot update vendor.')

    # Update status to inactive of port
    @transaction.atomic
    def delete(self, request, id):
        # Update port status to inactive
        port_service = PortService(data=request.data)
        if port_service.delete(id=id):
            return success_response(message="Port removed successfully")
        else:
            return success_response(message="Cannot remove port")

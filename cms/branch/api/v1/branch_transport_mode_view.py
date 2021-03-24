from branch.decorator import validate_branch_info, validate_transport_mode_id
from branch.models.branch_transport_mode import BranchTransportMode
from branch.serializers import BranchTransportModeSerializer, BranchTransportModeBaseSerializer
from branch.services.branch_service import BranchTransportModeService
from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import api_view
from utils.base_models import StatusBase
from utils.responses import success_response, error_response


class BranchTransportModeView(generics.GenericAPIView):
    serializer_class = BranchTransportModeSerializer

    @validate_branch_info
    @transaction.atomic
    def post(self, request, company_id, branch_id):
        data = request.data    
        data['branch'] = branch_id
        serializer = BranchTransportModeBaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Branch transport mode added successfully')
        return error_response(data=serializer.errors)

    # Get all branch transport mode details based on branch_id
    def get(self, request, company_id, branch_id):

        branch_transport_mode_service = BranchTransportModeService(
            data=request)
        result = branch_transport_mode_service.get(branch_id=branch_id)
        if result:
            return success_response(message="Branch transport mode details retrieved successfully.", data=result)
        else:
            return success_response(message="No more records")


class BranchTransportModeDetailView(generics.GenericAPIView):
    serializer_class = BranchTransportModeSerializer

    def get(self, request, company_id, branch_id, id):

        branch_transport_mode_service = BranchTransportModeService({})
        result = branch_transport_mode_service.get(branch_id=branch_id, id=id)

        return success_response(message="Branch transport mode detail is retrieved successfully.", data=result)

    @validate_transport_mode_id
    @transaction.atomic
    def delete(self, request, company_id, branch_id, id): 
        branch_transport_mode_data = BranchTransportMode.objects.get(branch_id=branch_id, id=id, status=StatusBase.ACTIVE)
        branch_transport_mode_data.delete()
        return success_response(message="Branch transport mode deleted successfully")

    @validate_transport_mode_id
    @transaction.atomic
    def put(self, request, company_id, branch_id, id):
        data = request.data    
        data['branch'] = branch_id    
        transport_mode_object = BranchTransportMode.objects.get(branch=branch_id, id=id)
        serializer = BranchTransportModeBaseSerializer(transport_mode_object, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Branch transport mode updated successfully")
        return error_response(data=serializer.errors)

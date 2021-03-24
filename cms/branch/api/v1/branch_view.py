from branch.decorator import validate_branch_info
from branch.models.branch import Branch
from branch.serializers import BranchSerializer, BranchBaseSerializer, BranchDeleteSerializer, BranchUpdateSerializer
from branch.services.branch_service import BranchService
from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import api_view
from utils.responses import success_response, error_response


class BranchView(generics.GenericAPIView):
    serializer_class = BranchSerializer

    @transaction.atomic
    def post(self, request, company_id):
        data = request.data    
        data['company'] = company_id
        serializer = BranchBaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Branch created successfully')
        return error_response(data=serializer.errors)


    def get(self, request, company_id):

        branch_service = BranchService(data=request)
        result = branch_service.get(company_id=company_id)
        if result:

            return success_response(message='Branch data retrived successfully', data=result)
        else:
            return success_response(message='No more records')


class BranchDetailView(generics.GenericAPIView):

    def get(self, request, company_id, branch_id):

        branch_service = BranchService(data=request)
        result = branch_service.get(company_id=company_id, id=branch_id)
        return success_response(message='Branch data retrived successfully', data=result)
        

    @validate_branch_info
    @transaction.atomic
    def put(self, request, company_id, branch_id):
        data = request.data
        data['company']=company_id     
        branch_object = Branch.objects.get(company=company_id, id=branch_id)
        serializer = BranchUpdateSerializer(branch_object, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Branch updated successfully")
        return error_response(data=serializer.errors)


    @validate_branch_info
    @transaction.atomic   
    def delete(self, request, company_id, branch_id):
        data = {'company':company_id, 'branch_id':branch_id}
        serializer = BranchDeleteSerializer(data=data)

        if serializer.is_valid():

            data = serializer.validated_data
            Branch.services.delete(company_id=company_id, branch_id=branch_id, parent_id=data['parent_id'])
            return success_response(message="Branch removed successfully")
        
        return error_response(data=serializer.errors)


class BranchTransferView(generics.GenericAPIView):

    @transaction.atomic
    def delete(self, request, company_id):
        branch_servive = BranchService({})
        result = branch_servive.transfer_vendor_branch(
            request.data, company_id)
        if result:
            return success_response(message="Reassigned users to other branch successfully")
        else:
            return success_response(message="User has failed to reassign to another branch")

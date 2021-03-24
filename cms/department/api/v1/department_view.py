from customer.services.customer_manage_service import CustomerManageService
from department.decorator import validate_department_info
from department.models.department import Department
from department.serializers import DepartmentSerializer, DepartmentValidateSerializer
from department.services.department_service import DepartmentService
from django.db import transaction
from exceptions.department_exceptions import DepartmentException, DepartmentError
from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from utils.base_models import StatusBase
from utils.responses import success_response , get_paginated_data, error_response

class DepartmentView(generics.GenericAPIView):
    serializer_class = DepartmentSerializer

    '''To add new department'''

    @transaction.atomic
    def post(self, request, company_id):

        data = request.data    
        data['company']=company_id
        serializer = DepartmentValidateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Department created successfully')
        return error_response(data=serializer.errors)

    '''to get all department which are active'''

    @transaction.atomic
    def get(self, request, company_id):
        
        departments = Department.find_by(
            multi=True, join=False, status=StatusBase.ACTIVE, company_id=company_id).order_by('name')
        
        department_paginated_data = get_paginated_data(DepartmentSerializer, departments, request)

        # Get department list with user count
        department_paginated_data = DepartmentService.get_department_list_with_user_count(department_paginated_data)

        if department_paginated_data:
            return success_response(message="Department data retrived successfully", data=department_paginated_data)
        else:
            return success_response(message='No more records')


class DepartmentDetailView(generics.GenericAPIView):
    '''get department details based on department id'''
    serializer_class = DepartmentSerializer
    
    @transaction.atomic
    def get(self, request, company_id, department_id):
        
        department = Department.find_by(
            multi=True, join=False, status=StatusBase.ACTIVE, id=department_id, company_id=company_id)
        if not department:
            raise DepartmentException(DepartmentError.DEPARTMENT_NOT_FOUND)

        department_serializer = DepartmentSerializer(
            department, many=True)

        return success_response(message="Department Data retrived successfully", data=department_serializer.data[0])

    '''edit the department details based on id'''

    @validate_department_info
    @transaction.atomic
    def put(self, request, company_id, department_id):

        data = request.data
        data['company']=company_id     
        department_object = Department.objects.get(company=company_id,id=department_id)
        serializer = DepartmentValidateSerializer(department_object, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Department updated successfully")
        return error_response(data=serializer.errors)


    '''soft delete the department'''
    @validate_department_info
    @transaction.atomic
    def delete(self, request, company_id, department_id):
        department_data = Department.services.delete_department(company_id=company_id, department_id=department_id)
        if department_data:
            return success_response(message="Department deleted successfully")
        return error_response(message="You can not delete department")
        


@api_view(['GET'])
@transaction.atomic
def customer_list_by_department_id(request, company_id, department_id):
    result = CustomerManageService.customer_list_by_department_id(request, company_id, department_id)
    if result:
        return success_response(message="Customer Data retrieved successfully.", data=result)
    else:
        return success_response(message="Customer data not found.")

@api_view(['PUT'])
@transaction.atomic
def reassigned_users_to_other_department(request, company_id, id):
    department_detail = DepartmentService.transfer_department_user(request.data, company_id, id)
    if department_detail:
        return success_response(message="Reassigned users to other department successfully")
    else:
        return success_response(message="Reassigned users to other department failure")

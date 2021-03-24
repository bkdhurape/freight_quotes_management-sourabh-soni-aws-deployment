from company.models.company import Company
from customer.models.customer import Customer
from department.models.department import Department
from department.serializers import DepartmentSerializer
from django.core.exceptions import ObjectDoesNotExist
from exceptions.department_exceptions import DepartmentException, DepartmentError
from utils.base_models import StatusBase
from utils.responses import success_response
from company.services.company_service import CompanyService


class DepartmentService:

    department_list = ['Accounts', 'Logistics',
                       'Purchase', 'Supply_chain', 'Management']

    def __init__(self, data):
        self.data = data

    def check_department_company(self, departments):
        '''loop through object and check company exists with given department name'''
        for company in departments:
            if self.data['company'] == company['company_id']:
                if company['status'] == 1:
                    raise DepartmentException(
                        DepartmentError.DEPARTMENT_EXISTS)
                else:
                    Department.objects.filter(id=company['id']).update(
                        status=StatusBase.ACTIVE)
                # check status or raise exception
                return True
        return False

    def check_department_exist(self):
        department = Department.find_by(
            multi=True, join=False, name=self.data['name'])
        if department:
            department_details = department.values()
            company_id_exists = self.check_department_company(
                departments=department_details)
            if company_id_exists:
                return True
            else:
                return False
        else:
            return False

    def create_default_department(self, request=None, company_id=None):
        if company_id:
            for department_name in self.department_list:
                department_serializer = DepartmentSerializer(
                    data={'name': department_name, 'company': company_id, 'type': Department.DEFAULT})

                if department_serializer.is_valid(raise_exception=True):
                    department_serializer.save()
        return True

    def create(self, company_id=None):
        if company_id:
            if self.create_default_department(company_id=company_id):
                return True
        
        CompanyService.get(self,id=self.data['company'])

        department_serializer = DepartmentSerializer(data=self.data)
        department = self.check_department_exist()

        if not department and department_serializer.is_valid(raise_exception=True):
            department_serializer.save()
        return True

    def update(self, department_id, company_id):
        department_object = Department.find_by(
            multi=False, join=False, id=department_id, company_id=company_id)
        department_serializer = DepartmentSerializer(
            department_object, data=self.data)
        if department_serializer.is_valid(raise_exception=True):
            department_serializer.save()

    # Update department status to inactive
    def delete_department(self, company_id, id):
        departments = Department.find_by(
            multi=True, join=True, status=StatusBase.ACTIVE, id=id, company_id=company_id)

        if not departments:
            raise DepartmentException(DepartmentError.DEPARTMENT_NOT_FOUND)
        active_customers = Customer.find_by(multi=True, department=id, status=StatusBase.ACTIVE)

        if active_customers.count():
            return False
        else:
            DepartmentService.update_department_status(departments)
            return True


    # Transfer user to other department 
    def transfer_department_user(request_data, company_id, id):

        departments = Department.find_by(
            multi=True, join=True, status=StatusBase.ACTIVE, id=id, company_id=company_id)

        if not departments:
            raise DepartmentException(DepartmentError.DEPARTMENT_NOT_FOUND)

        for user in request_data:
            if id in user['department']:
                user['department'].remove(id)

            exist_department_list = list(Customer.find_by(multi=True, id=user['id'], status=StatusBase.ACTIVE).values_list('department', flat=True))
            update_department_list = user['department']

            remove_list = [item for item in exist_department_list if item not in set(update_department_list)]
            add_list = [item for item in update_department_list if item not in set(exist_department_list)]

            # Remove Mapping
            if remove_list:
                for department_id in remove_list:
                    customer = Customer.find_by(id=user['id'], department=department_id, status=StatusBase.ACTIVE)
                    department = Department.find_by(id=department_id, status=StatusBase.ACTIVE)
                    customer.department.remove(department)
                    
            # Add Mapping
            if add_list:
                for department_id in add_list:
                    customer = Customer.find_by(id=user['id'], status=StatusBase.ACTIVE)
                    department = Department.find_by(id=department_id, status=StatusBase.ACTIVE)
                    customer.department.add(department)

        return True

    def update_department_status(departments):
        for department in departments:
            department.status = StatusBase.INACTIVE
            department.save()


    def get_department_list_with_user_count(department_list):
        for department_detail in department_list:
            count = Customer.find_by(multi=True, department=department_detail['id'], status=StatusBase.ACTIVE).count()
            department_detail.update({'count': count})
        return department_list

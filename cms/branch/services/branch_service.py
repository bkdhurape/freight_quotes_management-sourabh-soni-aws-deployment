from branch.models.branch import Branch
from branch.serializers import BranchSerializer
from branch.services.branch_transport_mode_service import BranchTransportModeService
from company.models.company import Company
from company.services.company_service import CompanyService
from django.conf import settings
from exceptions import BranchException, BranchError
from utils.base_models import StatusBase
from utils.responses import get_paginated_data
from vendor.models.vendor import Vendor
from vendor.models.vendor_type import VendorType
from vendor.serializers import VendorSerializer
from vendor.services.vendor_service import VendorService
import pint
ureg = pint.UnitRegistry()


class BranchService:

    def __init__(self, data):
        self.data = data

    # Create new branch based on company id
    def create(self, company_id=None):

        branch_serializer = BranchSerializer(data=self.data)
        company_id = self.data['company']
        
        if self.data['name'] != 'HQ':
            vendor_type = list(Vendor.find_by(
                multi=True, home_company_id=company_id, status=Vendor.ACTIVE).values_list('vendor_type', flat=True))[0]

            if vendor_type == 'transport-only':

                # Required field weight and radius validation function
                self.weight_and_radius_validations()

                # Unit conversion function of weight and radius
                self.weight_and_radius_unit_conversion()
               
                             
            else:
                self.data['minimum_weight']=None
                self.data['maximum_weight']=None
                self.data['weight_unit']=None
                self.data['minimum_radius']=None
                self.data['maximum_radius']=None
                self.data['radius_unit']=None

        if branch_serializer.is_valid(raise_exception=True):
            branch_id = branch_serializer.save().id
            return branch_id

    def weight_and_radius_validations(self):

        if('minimum_weight' not in self.data or not self.data['minimum_weight']):
            raise BranchException(BranchError.MINIMUM_WEIGHT_REQUIRED)

        if('maximum_weight' not in self.data or not self.data['maximum_weight']):
            raise BranchException(BranchError.MAXIMUM_WEIGHT_REQUIRED)

        if (('minimum_weight' in self.data and self.data['minimum_weight']) and ('weight_unit' not in self.data or not self.data['weight_unit'])):
            raise BranchException(BranchError.WEIGHT_UNIT_REQUIRED)
        
        if (('maximum_weight' in self.data and self.data['maximum_weight']) and ('weight_unit' not in self.data or not self.data['weight_unit'])):
            raise BranchException(BranchError.WEIGHT_UNIT_REQUIRED)

        if (('minimum_weight' in self.data and self.data['minimum_weight']) >= ('maximum_weight' in self.data and self.data['maximum_weight'])):
            raise BranchException(BranchError.MAXIMUM_WEIGHT_SHOULD_BE_GREATER)

        if('minimum_radius' not in self.data or not self.data['minimum_radius']):
            raise BranchException(BranchError.MINIMUM_RADIUS_REQUIRED)

        if('maximum_radius' not in self.data or not self.data['maximum_radius']):
            raise BranchException(BranchError.MAXIMUM_RADIUS_REQUIRED)

        if (('minimum_radius' in self.data and self.data['minimum_radius']) and ('radius_unit' not in self.data or not self.data['radius_unit'])):
            raise BranchException(BranchError.RADIUS_UNIT_REQUIRED)       

        if (('maximum_radius' in self.data and self.data['maximum_radius']) and ('radius_unit' not in self.data or not self.data['radius_unit'])):
            raise BranchException(BranchError.RADIUS_UNIT_REQUIRED)

        if (('minimum_radius' in self.data and self.data['minimum_radius']) >= ('maximum_radius' in self.data and self.data['maximum_radius'])):
            raise BranchException(BranchError.MAXIMUM_RADIUS_SHOULD_BE_GREATER)

    def weight_and_radius_unit_conversion(self):

        # Converting minimum weight to kg
        minimum_weight = ureg(str(self.data['minimum_weight'])+self.data['weight_unit'])
        minimum_weight_to_kg = minimum_weight.to('kg')
        new_minimum_weight_kg = round((minimum_weight_to_kg.magnitude),3)                
        self.data['minimum_weight_kg'] = new_minimum_weight_kg

        # Converting maximum weight to kg
        maximum_weight = ureg(str(self.data['maximum_weight'])+self.data['weight_unit'])
        maximum_weight_to_kg = maximum_weight.to('kg')
        new_maximum_weight_kg = round((maximum_weight_to_kg.magnitude),3)
        self.data['maximum_weight_kg'] = new_maximum_weight_kg 

        # Converting minimum radius to km
        minimum_radius = ureg(str(self.data['minimum_radius'])+self.data['radius_unit'])
        minimum_radius_to_km = minimum_radius.to('km')
        new_minimum_radius_km = round((minimum_radius_to_km.magnitude),3)
        self.data['minimum_radius_km'] = new_minimum_radius_km

        # Converting maximum radius to km
        maximum_radius = ureg(str(self.data['maximum_radius'])+self.data['radius_unit'])
        maximum_radius_to_km = maximum_radius.to('km')
        new_maximum_radius_km = round((maximum_radius_to_km.magnitude),3)              
        self.data['maximum_radius_km'] = new_maximum_radius_km

        

    # Get all branch and get branch by id
    def get(self, company_id, id=None):

        # CompanyService.get(self, id=company_id)
        filter_params = {'company_id': company_id}
        if id is not None:
            filter_params.update({'id': id})
        if id is None:
            filter_params.update({'parent': None})

  
        branches_data = Branch.objects.filter(status=StatusBase.ACTIVE, **filter_params).values('id','name')
        if not branches_data:
            raise BranchException(BranchError.BRANCH_NOT_FOUND)
        
        vendor_branch_ids = [i['id'] for i in branches_data]

        result_list = []

        def get_children_data(branch_id):
            branch_dict = {}
            branch_obj = BranchSerializer(Branch.objects.get(id=branch_id, status=Branch.ACTIVE), fields=('id', 'name')).data
            branch_dict.update(branch_obj)

            has_children = list(Branch.objects.filter(parent=branch_obj['id'], status=Branch.ACTIVE).values())
            if has_children:
                child_list = []
                for child in has_children:
                    child_id = child['id']
                    child_result = get_children_data(child_id)
                    child_list.append(child_result)
                branch_dict.update({'children': child_list})

            return branch_dict

        for branch_data in vendor_branch_ids:
            result = get_children_data(branch_data)
            result_list.append(result)
        
        branch_paginated_data = get_paginated_data(
            BranchSerializer, result_list, self.data, id, serialized_data=True)

        return branch_paginated_data

    # Update branch based on company id and branch id
    def update(self, company_id, id):
        CompanyService.get(self, id=company_id)
        branch = Branch.find_by(
            multi=False, join=False, status=StatusBase.ACTIVE, company_id=company_id, id=id)

        if 'name' in self.data:
            self.data['company'] = company_id
            branch_serializer = BranchSerializer(branch, data=self.data)
            if branch_serializer.is_valid(raise_exception=True):
                branch_serializer.save()

        return True

    # Soft delete branch with branch transport mode
    def delete(self, company_id, id):
        CompanyService.get(self, id=company_id)
        branch = Branch.find_by(
            multi=True, join=False, status=StatusBase.ACTIVE, company_id=company_id, id=id)

        if not branch:
            raise BranchException(BranchError.BRANCH_NOT_FOUND)

        branch_serializer = BranchSerializer(branch, many=True)
        branch_data = branch_serializer.data[0]

        if branch_data['is_head_branch'] == True:
            raise BranchException(BranchError.HEAD_BRANCH_CANT_DELETE)

        vendors = Vendor.find_by(
            multi=True, branch=id, status=StatusBase.ACTIVE)

        if vendors.count():
            return False
        else:
            self.delete_branch(branch, company_id, id)
            return True

    def delete_branch(self, branch, company_id, branch_id):

        branch_serializer = BranchSerializer(branch, many=True)
        parent_id = branch_serializer.data[0]['parent']

        # calling branch transport mode inactive and branch inactive function
        self.get_branch_childrens(branch_id, company_id, parent_id)
        self.delete_branch_transport_mode(branch_id)
        self.inactive_branch(branch_id)

    def inactive_branch(self, branch_id):
        branch_data = Branch.find_by(id=branch_id)
        branch_data.status = StatusBase.INACTIVE
        branch_data.save()

    # Inactive branch transport mode
    def delete_branch_transport_mode(self, branch_id):
        branch_transport_details_service = BranchTransportModeService(
            data=self.data)
        branch_transport_details = branch_transport_details_service.get(
            branch_id, action = 'delete')
        
        if branch_transport_details:
            for branch_transport_detail in branch_transport_details:
                branch_transport_detail_service = BranchTransportModeService({})
                branch_transport_detail_service.delete(branch_id, 
                                                    branch_transport_detail['id'])

    def get_branch_childrens(self, id, company_id, parent_id):

        branch = Branch.find_by(multi=True, join=False,
                                parent_id=id, company_id=company_id)

        if branch.count():
            branch_serializer = BranchSerializer(branch, many=True)
            for branch in branch_serializer.data:
                self.update_branch_parent(
                    branch['id'], company_id, parent_id, branch['name'], branch['country'])

    def update_branch_parent(self, id, company_id, parent_id, name, country):

        branch_update_obj = {}
        branch_update_obj.update(
            {'name': name, 'company': company_id, 'parent': parent_id, 'country': country})

        self.data = branch_update_obj

        self.update(company_id, id)

    def transfer_vendor_branch(self, request_data, company_id):

        Company.find_by(id=company_id)

        for vendor in request_data:
            # Get vendor by company and vendor id
            vendor_data = Vendor.find_by(
                multi=False, home_company=company_id, id=vendor['id'])

            # Iterate over all the branch id and check if that branch belong to the company
            for branch_id in vendor['branch']:
                Branch.find_by(multi=False, status=StatusBase.ACTIVE,
                               id=branch_id, company_id=company_id)

            vendor_serializer = VendorSerializer(vendor_data)
            vendor_update_data = vendor_serializer.data

            # Update vendor data dictionary 'branch' key by new branch values
            vendor_update_data.update({'branch': vendor['branch']})

            # Call service to update vendor branch data
            vendor_service = VendorService(data=vendor_update_data)
            vendor_service.update(vendor['id'])

        return True

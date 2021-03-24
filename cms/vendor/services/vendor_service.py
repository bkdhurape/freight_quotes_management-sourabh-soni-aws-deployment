from branch.models.branch import Branch
from company.models.company import Company
from currency.services.currency_profile_service import CurrencyProfileService
from django.conf import settings
from exceptions import VendorException, VendorError
from utils.helpers import encode_data
from utils.responses import get_paginated_data
from vendor.models.vendor import Vendor
from vendor.models.vendor_companies_mode import VendorCompaniesMode
from vendor.serializers import VendorSerializer, VendorCompaniesModeSerializer, VendorDetailSerializer

class VendorService:

    def __init__(self, data):
        self.data = data

    def update(self, vendor_id):

        vendor = Vendor.find_by_ids(id=vendor_id)
        self.data['id'] = vendor_id
        vendor_serializer = VendorSerializer(vendor, data=self.data)
        if vendor_serializer.is_valid(raise_exception=True):
            vendor_serializer.save()

    # Update vendor status to inactive
    def delete(vendor_id):
        vendor = Vendor.find_by(id=vendor_id, status=Vendor.ACTIVE)
        vendor.status = Vendor.INACTIVE
        vendor.save()

    # Get all vendor details with vendor & currency details
    def get_vendor_details(self, request, company_id):
        result = []
        Company.find_by(id=company_id)
        vendor_data = Vendor.find_by(multi=True, join=False, home_company=company_id, status=Vendor.ACTIVE).order_by('-id')

        vendor_paginated_data = get_paginated_data(VendorDetailSerializer, vendor_data, self.data)

        if vendor_paginated_data:
            
            for vendor in vendor_paginated_data:
                id = int(vendor['id'])
                currency_profile_dicts = CurrencyProfileService.get_currency_profile(entity_type='vendor',
                                                                                    entity_id=id)
                companies_mode_dicts = VendorService.get_companies_mode(id)

                encoded_email = encode_data(vendor['email'])
                vendor['send_link'] = resend_link = settings.API_HOST + '/api/v1/company/' + str(vendor['home_company']) + '/vendor/send_activation_link/' + encoded_email

                result.append({
                        'vendor_data': vendor,
                        'currency_profile_data': currency_profile_dicts,
                        'companies_mode_data': companies_mode_dicts
                    })

            return result
        else :
            return False

    # Get vendor & currency profile data by vendor ID
    def get_vendor_detail_by_id(company_id, id):
        Company.find_by(id=company_id)
        vendor_data = Vendor.find_by(multi=True, join=False, id=id, home_company=company_id, status=Vendor.ACTIVE)
        if not vendor_data:
            return False

        vendor_serializer = VendorDetailSerializer(vendor_data, many=True)
        vendor = vendor_serializer.data[0]

        currency_profile_dicts = CurrencyProfileService.get_currency_profile(entity_type='vendor', entity_id=id)
        companies_mode_dicts = VendorService.get_companies_mode(id)

        result = {
            'vendor_data': vendor,
            'currency_profile_data': currency_profile_dicts,
            'companies_mode_data': companies_mode_dicts
        }

        return result


    # Check company branch exist or not
    def company_branch_exist(company_id, branch_id_list):
        Company.find_by(id=company_id, status=Vendor.ACTIVE)

        for branch_id in branch_id_list:
            branch_exist = Branch.find_by(multi=True, company=company_id, id=branch_id)
            if not branch_exist:
                raise VendorException(VendorError.VENDOR_COMPANY_BRANCH_NOT_EXISTS)

    # Fetch Vendor multiple compnies mode data
    def get_companies_mode(vendor_id):
        vendor_object = VendorCompaniesMode.find_by(vendor=vendor_id, multi=True)
        vendor_companies_mode_serializer = VendorCompaniesModeSerializer(vendor_object, many=True)
        return vendor_companies_mode_serializer.data if len(vendor_companies_mode_serializer.data) > 0 else {}
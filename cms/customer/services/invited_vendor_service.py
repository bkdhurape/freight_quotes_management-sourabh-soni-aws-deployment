from company.models.company import Company
from customer.models.customer import Customer
from customer.models.invited_vendor import InvitedVendor
from customer.serializers import InvitedVendorSerializer
from customer.services.customer_manage_service import CustomerManageService
from django.conf import settings
from exceptions import InvitedVendorException, InvitedVendorError
from utils.base_models import StatusBase
from utils.responses import get_paginated_data
from utils.helpers import encode_data
from vendor.models.vendor import Vendor


class InvitedVendorService:

    def __init__(self, data):
        self.data = data

    #  Get all company vendors(clients)
    def get_all(self, company_id, user_id, user_type = 'customer'):
        Company.find_by(id = company_id, user_type=user_type, status = StatusBase.ACTIVE)

        if user_type == 'customer':
            Customer.find_by(id = user_id, home_company = company_id, status = StatusBase.ACTIVE)
            filter_params = {'customer_company_id': company_id}
            company_key = 'vendor_company'
        else:
            Vendor.find_by(id = user_id, home_company = company_id, status = StatusBase.ACTIVE)
            filter_params = {'vendor_company_id': company_id}
            company_key = 'customer_company'


        invited_vendors = InvitedVendor.find_by(multi = True, **filter_params)
        invited_vendor_paginated_data = get_paginated_data(InvitedVendorSerializer, invited_vendors, self.data)

        if invited_vendor_paginated_data:

            for data in invited_vendor_paginated_data:
                company_data = Company.find_by(multi = True, id = data[company_key], status = StatusBase.ACTIVE)
                if company_data:
                    data['company_name'] = list(company_data.values_list('name', flat = True))[0]
                if data['status'] == 2:
                    data['action'] = 'PENDING'
                else:
                    data['action'] = 'ACTIVE' if data['status'] == 1 else 'REJECTED'

            return invited_vendor_paginated_data

        return False


    #  Company  - Add Vendor ( as Client)
    def create(self, customer_company_id, customer_id):
        Company.find_by(id = customer_company_id, status = StatusBase.ACTIVE)
        Customer.find_by(id = customer_id, status = StatusBase.ACTIVE)

        invite_data = self.data

        self.data['customer'] = customer_id
        self.data['customer_company'] = customer_company_id
        self.data['vendor_company'] = None
        self.data['vendor'] = None

        vendor_company_id = self.check_and_get_company_id_by_name()

        if vendor_company_id:
            self.data['vendor_company'] = vendor_company_id
            vendor_id = self.check_and_get_vendor_id_by_email_and_company(company_id = vendor_company_id)

            if vendor_id:
                self.data['vendor'] = vendor_id

                self.save_vendor()
                response = {'status': 'success',
                            'data': None}
            else:
                vendor_id = self.get_vendor_super_admin_id(company_id = vendor_company_id)
                self.data['vendor'] = vendor_id if vendor_id else None
                self.save_vendor()

                del invite_data['customer']
                del invite_data['customer_company']
                del invite_data['vendor_company']
                del invite_data['vendor']

                response = {'status': 'success', 'data': invite_data}

        else:
                invitation_link = self.save_vendor(send_invitation_link = True)
                response = {'status': 'success',
                            'data': invitation_link}

        return response


    # Save Invited Vendor
    def save_vendor(self, send_invitation_link = False):
        invited_vendor_serializer = InvitedVendorSerializer(data = self.data)
        if invited_vendor_serializer.is_valid(raise_exception=True):
            invited_vendor_id = (invited_vendor_serializer.save()).id
            if send_invitation_link:
                invitation_link = self.create_invitation_link(invited_vendor_id)

                return invitation_link

        return True


    #  Get client by id
    def get(self, id):
        invited_vendor = InvitedVendor.find_by(multi=False, id=id)
        invited_vendor_serializer = InvitedVendorSerializer(invited_vendor)

        return invited_vendor_serializer.data


    #  Update client by id
    def update(self, id):
        invited_vendor = InvitedVendor.find_by(id=id)
        invited_vendor_serializer = InvitedVendorSerializer(invited_vendor, data=self.data)
        if invited_vendor_serializer.is_valid(raise_exception=True):
            invited_vendor_serializer.save()

        return True

    #  Update client by id
    def update_status(self, vendor_company_id, vendor_id, id, action):

        if action not in ['accept','reject']:
            raise InvitedVendorException(InvitedVendorError.CLIENT_ACTION_REQUIRED)

        vendor = Vendor.find_by(multi = True, id = vendor_id, home_company = vendor_company_id, is_super_admin=True, status = StatusBase.ACTIVE)

        invited_vendor = InvitedVendor.find_by(multi = True, id = id)
        if invited_vendor:
            invited_vendor_serializer = InvitedVendorSerializer(invited_vendor, many = True)
            invited_vendor_data = invited_vendor_serializer.data[0]

            if not vendor and invited_vendor_data['vendor'] != vendor_id:
                raise InvitedVendorException(InvitedVendorError.CANNOT_ACCEPT_OR_REJECT_CLIENT)

            invited_vendor_data['status'] = InvitedVendor.ACTIVE if action == 'accept' else InvitedVendor.REJECT

            invited_vendor_service = InvitedVendorService(data=invited_vendor_data)
            invited_vendor_service.update(id)

        return True


    #  Delete invited vendor by id
    def delete(customer_company_id, customer_id, id):
        Company.find_by(id = customer_company_id, status = StatusBase.ACTIVE)
        Customer.find_by(id = customer_id, status = StatusBase.ACTIVE)

        customer = Customer.find_by(multi = True, id = customer_id, home_company = customer_company_id, is_super_admin=True, status = StatusBase.ACTIVE)

        invited_vendor = InvitedVendor.find_by(multi = True, id = id)
        if invited_vendor:
            invited_vendor_serializer = InvitedVendorSerializer(invited_vendor, many = True)
            invited_vendor_data = invited_vendor_serializer.data[0]

            if not customer and invited_vendor_data['customer'] != customer_id:
                raise InvitedVendorException(InvitedVendorError.INVITED_VENDOR_CANNOT_BE_DELETED)

            invited_vendor = InvitedVendor.find_by(id = id)
            invited_vendor.delete()


    # Check company exists by company name and get company id if exists
    def check_and_get_company_id_by_name(self):
        company = Company.find_by(multi = True, name = self.data['company_name'], user_type = 'vendor')

        if company:
            company_id = list(company.values_list('id', flat=True))[0]
            return company_id

        return False

    #  Check vendor exists by email and company id and get vendor id if exists
    def check_and_get_vendor_id_by_email_and_company(self, company_id):
        vendor = Vendor.find_by(multi = True, email = self.data['email'], home_company = company_id, status = Vendor.ACTIVE)

        if vendor:
            vendor_id = list(vendor.values_list('id', flat=True))[0]
            return vendor_id

        return False

    # Get vendor id of super admin by company id
    def get_vendor_super_admin_id(self, company_id):
        vendor = Vendor.find_by(multi = True, is_super_admin = True, home_company = company_id, status = Vendor.ACTIVE)
        if vendor:
            vendor_id = list(vendor.values_list('id', flat=True))[0]
            return vendor_id

        return False

    # Create registeration link with token to register new vendor and add this vendor as a client
    def create_invitation_link(self, invited_vendor_id):
        data = str(invited_vendor_id) + '__' + self.data['company_name'] + '__' + self.data['email']
        encoded_data = encode_data(data)
        link = settings.API_HOST + '/api/v1/vendor/' + encoded_data

        return link

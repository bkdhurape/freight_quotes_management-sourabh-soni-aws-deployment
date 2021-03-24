from contact_person.decorator import validate_contact_info
from contact_person.models.contact_person import ContactPerson
from contact_person.serializers import ContactPersonSerializer , ContactPersonBaseSerializer
from contact_person.services.contact_person_service import ContactPersonService
from django.db import transaction
from rest_framework import generics
from utils.base_models import StatusBase
from utils.responses import success_response, error_response


class ContactPersonView(generics.GenericAPIView):

    '''To add new contact person'''
    @transaction.atomic
    def post(self, request, company_id):
        data = request.data
        data['company'] = company_id
        serializer = ContactPersonBaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message='Contact person added successfully')
        return error_response(data=serializer.errors)


    '''to get all contact person based on type which are active'''
    def get(self, request, company_id, contact_person_type=ContactPerson.FINANCE):
        contact_person_service = ContactPersonService(data=request)
        result = contact_person_service.get_details(
            company_id=company_id, contact_person_type=contact_person_type)
        if result:
            return success_response(message="Contact details retrieved successfully.", data=result)
        else:
            return success_response(message="No more records")


class ContactPersonDetailView(generics.GenericAPIView):

    '''To get contact person based on company id and contact person id '''
    def get(self, request, company_id, contact_person_id, contact_person_type=ContactPerson.FINANCE):
        contact_person_service = ContactPersonService(data=request)
        result = contact_person_service.get_details_by_id(
            company_id=company_id, contact_person_id=contact_person_id, contact_person_type=contact_person_type)
        return success_response(message="Contact detail is retrieved successfully", data=result)
        

    '''To delete the contact person'''
    @validate_contact_info
    @transaction.atomic
    def delete(self, request, company_id, contact_person_id):
        contact_person_data = ContactPerson.objects.get(company=company_id, id=contact_person_id, status=StatusBase.ACTIVE)
        contact_person_data.status = StatusBase.INACTIVE
        contact_person_data.save()
        return success_response(message="Contact details deleted successfully")


    '''To update the contact person'''
    @validate_contact_info
    @transaction.atomic
    def put(self, request, company_id, contact_person_id):
        data = request.data
        data['company']=company_id     
        contact_person_data = ContactPerson.objects.get(company=company_id, id=contact_person_id)
        serializer = ContactPersonBaseSerializer(contact_person_data, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Contact details updated successfully")
        return error_response(data=serializer.errors)

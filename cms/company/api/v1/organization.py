from company.serializers import OrganizationSerializer
from company.services import OrganizationService
from rest_framework import generics
from utils.responses import success_response


class OrganizationView(generics.GenericAPIView):
    serializer_class = OrganizationSerializer
    '''Get all organization'''

    def get(self, request):
        organization = OrganizationService.get_all()
        return success_response(
            message="Organization Data retrived successfully",
            data=organization)


class OrganizationDetailView(generics.GenericAPIView):

    serializer_class = OrganizationSerializer
    '''To get companies details based on organization id'''

    def get(self, request, id):
        organization_service = OrganizationService(data=request)
        organization_details = organization_service.get(
            organization_id=id,
            fields=['id', 'name'])
        if organization_details:
            return success_response(message="Company Data retrived successfully",
                                data=organization_details)
        else:
            return success_response(message="No more records")

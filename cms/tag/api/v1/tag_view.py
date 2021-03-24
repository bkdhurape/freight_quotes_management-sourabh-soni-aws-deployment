from company.services.company_service import CompanyService
from exceptions.tag_exceptions import TagException, TagError
from rest_framework import generics
from tag.models.tag import Tag
from tag.serializers import TagSerializer
from tag.services.tag_services import TagService
from utils.base_models import StatusBase
from utils.responses import get_paginated_data, success_response


class TagView(generics.GenericAPIView):
    serializer_class = TagSerializer

    """Creating new tag based on company id """

    def post(self, request, company_id):
        data = request.data
        if 'name' in data:
            data['company'] = company_id
            tag = TagService(data=data)
            tag.create()
            return success_response(message="Tags created successfully")
        else:
            return success_response(message='Tag name is required!!!')

    """Get all tags based on company id """

    def get(self, request, company_id):

        company_service = CompanyService(data=request)
        company_service.get(id=company_id)

        tags = Tag.find_by(multi=True, join=False,
                           status=StatusBase.ACTIVE, company_id=company_id)
        if not tags:
            raise TagException(TagError.TAG_NOT_FOUND)

        tag_paginated_data = get_paginated_data(TagSerializer, tags, request)
        if tag_paginated_data:

            return success_response(message="Tag data retrived successfully", data=tag_paginated_data)
        else:
            return success_response(message="No more records")


class TagDetailView(generics.GenericAPIView):

    serializer_class = TagSerializer
    """Get tags based on company and tag id """

    def get(self, request, company_id, id):
        
        company_service = CompanyService(data=request)
        company_service.get(id=company_id)
        tag = Tag.find_by(
            multi=True, join=False, status=StatusBase.ACTIVE, id=id, company_id=company_id)
        if not tag:
            raise TagException(TagError.TAG_NOT_FOUND)

        tags_serializer = TagSerializer(tag, many=True)
        return success_response(message="Tag Data retrived successfully", data=tags_serializer.data[0])

    """Edit the details of tag based on company and tag id """

    def put(self, request, company_id, id):
        data = request.data
        if 'name' in data:
            data['company'] = company_id
            tag = TagService(data=data)
            tag_id = tag.update(
                tag_id=id, company_id=company_id)
            return success_response(message="Tag updated successfully", data=tag_id)
        else:
            return success_response(message="Tag name and id required", data=data)

    """ Deleting tag based on company and tag id"""

    def delete(self, request, company_id, id):
        tag = TagService(data={})
        result = tag.delete(tag_id=id, company_id=company_id)
        return success_response(message="Tag removed successfully", data=result)

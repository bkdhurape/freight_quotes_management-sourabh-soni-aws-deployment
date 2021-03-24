from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def success_response(data=None, message=None, status_code=status.HTTP_200_OK,
                     status='success'):
    return Response({
            "status": status,
            "data": data,
            "message": message,
            "code": status_code
        }, status=status_code)


def error_response(data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST,
                   status='error'):
    return Response({
        "status": status,
        "errors": data,
        "message": message,
        "code": status_code
    }, status=status_code)


def get_paginated_data(serializer, data, request_data, id=None, fields=None, serialized_data=None):

    if id is not None and serialized_data !=True:
        serializer_data = serializer(data[0], many=False, fields=fields)
        return serializer_data.data

    if id is not None and serialized_data == True:
        return data[0]

    current_page = request_data.GET.get('page')
    if request_data.GET.get('limit'):
        limit = request_data.GET.get('limit')
    else:
        limit = settings.PAGE_SIZE
    
    paginator = Paginator(data, limit)

    try:
        page = paginator.page(current_page)
    
    # If user does not put page number in url it will display first page with first page data
    except PageNotAnInteger:
        page = paginator.page(1)

    # If page is empty and there is no more records it will display no more records
    except EmptyPage:
        return False

    if serialized_data == True:
        return page.object_list
    else:
        serializer_data = serializer(page, many=True,  fields=fields)
        return serializer_data.data
        
def middleware_response(data=None, message=None, status_code=status.HTTP_200_OK, status='success'):
    response = success_response(data=data, message=message, status_code=status_code, status=status)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    return response

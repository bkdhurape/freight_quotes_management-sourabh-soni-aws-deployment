from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from .base_exceptions import BaseException
from utils.helpers import serializer_error_to_string
import logging
import traceback

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, BaseException):
            data = exc.to_dict()
            response = Response(data, status=exc.getHTTPCode())
        else:
            # validation error via model
            logger.error(
                "UNKNOWN EXCEPTION",
                extra={
                    "unkown_exception": {
                        "message": str(exc),
                        "traceback": ''.join(traceback.format_tb(exc.__traceback__))
                    }
                }
            )
            
            response = Response(
                {'status': 'failure', 'code': 'TEF0001', 'message': 'Technical Error: ' + str(exc)}, status=500)
    else:
        customized_response = serializer_error_to_string(response.data)

        logger.error(
            "VALIDATION EXCEPTION",
            extra={
                "validation_exception": {
                    "message": customized_response
                }
            }
        )
        response = Response(
            {'status': 'failure', 'code': 'BEF0001', 'data': response.data, 'message': customized_response}, status=400)

    return response
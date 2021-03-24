import socket
import logging
import json
logger = logging.getLogger('django')


class RequestLogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        self._initial_http_body = request.body 
    # this requires because for some reasons there is no way to access request.body in the 'process_response' method.

    def __call__(self, request):
        self.process_request(request=request)
        response = self.get_response(request)
        if request.path.startswith('/api/') and not request.path.endswith('healthcheck'):
            log_data = {
                'remote_address': request.META['REMOTE_ADDR'],
                'server_hostname': socket.gethostname(),
                'request_method': request.method,
                'request_path': request.get_full_path(),
                'response_status': response.status_code,
                'x-api-client': request.META.get("HTTP_X_API_CLIENT", ""),
                'body': self._initial_http_body
            }
            
            if hasattr(response, "data"):
                log_data.update({
                    'api_status': response.data.get('status', ''),
                    'api_status_code': response.data.get('code', '')
                })
            logger.info("request", extra=log_data)
        return response

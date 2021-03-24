from company.models.company import Company
from datetime import datetime
from django.conf import settings
from django.contrib.auth import logout
from login.models.jwt_token import JwtToken
from rest_framework import status
from utils.base_models import StatusBase
from utils.responses import middleware_response
import jwt, re

EXEMPT_URLS = []
EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEPT_URLS]


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.restrict_app = {
            'customer': ['vendor', 'branch'],
            'vendor': ['customer'],
        }

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try: 
            assert hasattr(request, 'user')
            path = request.path_info

            if not any(url.match(path) for url in EXEMPT_URLS):
                if ('Authorization' not in request.headers) or (not request.headers['Authorization']):
                    return middleware_response(message='Token missing in header.')
                else:
                    jwt_token_decode = jwt.decode(request.headers['Authorization'], settings.JWT_FCT_SECRET, algorithms=['HS256'], options={'verify_exp': False})
                    if (not JwtToken.find_by(multi=True, token_key=request.headers['Authorization'])) or (int(datetime.timestamp(datetime.now())) > jwt_token_decode['exp']):
                        logout(request)
                        JwtToken.find_by(multi=True, entity_id=jwt_token_decode['user_id'], entity_type=jwt_token_decode['account_type'], session_id=jwt_token_decode['session_id']).delete()
                        return middleware_response(message='Login again token expired.')
                    else:
                        split_url = path.split('/')
                        company_list = list(Company.find_by(multi=True, organization=jwt_token_decode['organization_id'], status=StatusBase.ACTIVE).values_list('id', flat=True))
                        if ( (('company' == split_url[3]) and ( ( (split_url[4]) and (not (int(split_url[4]) in company_list)) ) or ( (len(split_url) > 5 and split_url[5]) and (split_url[5] in self.restrict_app[jwt_token_decode['account_type']]) ) ) ) or 
                            ( ('organization' == split_url[3]) and ( (not split_url[4]) or (split_url[4]) and ( int(split_url[4]) != jwt_token_decode['organization_id']) ) ) or
                            (split_url[3] in self.restrict_app[jwt_token_decode['account_type']]) ):
                            return middleware_response(status_code=status.HTTP_403_FORBIDDEN, message='Access denied.')
            else:
                pass

        except Exception:
            return middleware_response(status_code=status.HTTP_403_FORBIDDEN, message='Invalid token.')
import logging
import time
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.db import connection
from rest_framework_simplejwt.tokens import AccessToken



logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s; %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        request_data = {
            'method'  : request.method,
            'ip_address' : request.META.get('REMOTE_ADDR'),
            'path':request.path
        }
        logger.info(request_data)


        # Calling a Procedure
        if request.path.startswith("/api"):
            auth_header = request.headers.get('Authorization')
            token = None
            if auth_header:
                token = auth_header.split(" ")[1]

            with connection.cursor() as cursor:
                if request.user is not None and str(request.user) != 'AnonymousUser':
                    print(str(request.user))
                    print(type(request.user))
                    # cursor.callproc('log_api_request',[str(request.user), str(request.method), str(request.path), str(request.META.get('REMOTE_ADDR'))])
                    cursor.execute("CALL log_api_request(%s, %s, %s, %s)", [str(request.user.id), str(request.method), str(request.path), str(request.META.get('REMOTE_ADDR'))])

                else:
                    if token is not None:
                        access_token_obj = AccessToken(token)
                        cursor.execute("CALL log_api_request(%s, %s, %s, %s)", [str(access_token_obj['user_id']), str(request.method), str(request.path), str(request.META.get('REMOTE_ADDR'))])
                    else:
                        #cursor.callproc('log_api_request',['Anonymous', str(request.method), str(request.path), str(request.META.get('REMOTE_ADDR'))])
                        cursor.execute("CALL log_api_request(%s, %s, %s, %s)", ['Anonymous', str(request.method), str(request.path), str(request.META.get('REMOTE_ADDR'))])

        response = self.get_response(request)

        duration = time.time() - start_time

        response_dict = {
            'status_code' : response.status_code,
            'duration' : duration
        }

        logger.info(response_dict)

        return response
    

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        logger.info("Request Received")
        print("ABSOLUTE PATH : ",request.build_absolute_uri())
        print("PATH : ",request.path)
        print("METHOD : ",request.method)
        print("QUERY PARAMS :", request.GET)
        print("URL WITH QUERY : ",request.get_full_path())

        if settings.MAINTENANCE_MODE:
            logger.warning("Application is in Maintenance Mode!")
            return HttpResponse('<h1>Application is in Maintenance Mode, Please Come back Later</h1>')

        response = self.get_response(request)

        return response
    

class IPBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(settings, 'BANNED_IPS') and settings.BANNED_IPS is not None:
            if request.META['REMOTE_ADDR'] in settings.BANNED_IPS:
                raise PermissionDenied()
            

        response = self.get_response(request)
        return response
    

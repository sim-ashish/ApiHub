import logging
import time
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.cache import cache



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
        print("Request's IP : ", request.META['REMOTE_ADDR'])
        if hasattr(settings, 'BANNED_IPS') and settings.BANNED_IPS is not None:
            if request.META['REMOTE_ADDR'] in settings.BANNED_IPS:
                raise PermissionDenied()
            

        response = self.get_response(request)
        return response
    

class RateLimitingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user_ip = request.META.get('REMOTE_ADDR')
        request_count = cache.get(user_ip, 0)
        if request_count > 200:
            return HttpResponse("Too Many requests", status = 429)
        
        cache.set(user_ip, request_count + 1, timeout = 60)     # allow 1 request per minute
        response = self.get_response(request)
        return response
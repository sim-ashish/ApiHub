from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription  # Your Subscriber model
from rest_framework.exceptions import Throttled
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from api.tasks import subscription_mail
from rest_framework.permissions import IsAuthenticated


class CustomThrottle(BaseThrottle):
    # Defining throttling limits
    RATE_LIMITS = {
        'anonymous': 30,  # 30 requests/day for anonymous users
        'authenticated': 80,  # 80 requests/day for authenticated users
        'subscribed': 1000,  # 1000 requests/day for subscribers
    }
    def get_cache_key(self, request, view):
        '''Returns unique ip address'''
        return self.get_ident(request)

    def get_rate_limit(self,request):
        """Return the rate limit based on user type."""

        auth_header = request.headers.get('Authorization')
        token = None
        if auth_header:
             token = auth_header.split(" ")[1]
        if token == None:
            return self.RATE_LIMITS['anonymous']
        access_token_obj = AccessToken(token)
        user_id=access_token_obj['user_id']
        try:
            user=User.objects.get(id=user_id)
        except:
            return self.RATE_LIMITS['anonymous']
        if user.is_authenticated:
            # Check if the user is a subscriber
            if Subscription.objects.filter(user=user).exists():
                return self.RATE_LIMITS['subscribed']
            else:
                return self.RATE_LIMITS['authenticated']
        else:
            return self.RATE_LIMITS['anonymous']

    def allow_request(self, request, view):
        """Check if the request should be allowed or throttled."""
        user = None
        user_id = None
        auth_header = request.headers.get('Authorization')
        token = None
        if auth_header:
             token = auth_header.split(" ")[1]
        if token is not None:
            access_token_obj = AccessToken(token)
            user_id=access_token_obj['user_id']
        try:
            if user_id is not None:
                user=User.objects.get(id=user_id)
            else:
                raise Exception
        except:
            user = None
        
        key = self.get_cache_key(request, view)

        # Get the throttle limit based on the user
        rate_limit = self.get_rate_limit(request)
        current_time = timezone.now()
        cache_value = cache.get(key)

        # If there is no cache value, initialize the request count and timestamp
        if not cache_value:
            cache.set(key, {
                'count': 1,
                'timestamp': current_time,
            }, timeout=timedelta(days=1).total_seconds())
            return True

        # If the count is within the allowed limit, allow the request
        if cache_value['count'] < rate_limit:
            cache.set(key, {
                'count': cache_value['count'] + 1,
                'timestamp': current_time,
            }, timeout=timedelta(days=1).total_seconds())
            return True

        # If authenticated user exceeds the limit, send an email notification
        if user and cache_value['count'] >= self.RATE_LIMITS['authenticated']:
            subscription_mail.delay('krushanuinfolabz@gmail.com', user.email, user.id)

        # If exceeded the rate limit, throttle the request
        raise Throttled(detail=f"Rate limit exceeded: {rate_limit} requests per day.")
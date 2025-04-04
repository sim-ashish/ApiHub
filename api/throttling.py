from rest_framework.throttling import BaseThrottle
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription  # Your Subscriber model
from rest_framework.exceptions import Throttled

class CustomThrottle(BaseThrottle):
    # Define throttling limits
    RATE_LIMITS = {
        'anonymous': 50,  # 50 requests/day for anonymous users
        'authenticated': 100,  # 100 requests/day for authenticated users
        'subscribed': 1000,  # 1000 requests/day for subscribers
    }

    def get_rate_limit(self, user):
        """Return the rate limit based on user type."""
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
        user = request.user if request.user.is_authenticated else None
        key = self.get_cache_key(request, view)

        # If no cache key exists (first request), allow the request
        if not key:
            return True

        # Get the throttle limit based on the user
        rate_limit = self.get_rate_limit(user)
        current_time = timezone.now()
        cache_value = self.cache.get(key)

        # If there is no cache value, initialize the request count and timestamp
        if not cache_value:
            self.cache.set(key, {
                'count': 1,
                'timestamp': current_time,
            }, timeout=timedelta(days=1).total_seconds())
            return True

        # If the count is within the allowed limit, allow the request
        if cache_value['count'] < rate_limit:
            self.cache.set(key, {
                'count': cache_value['count'] + 1,
                'timestamp': current_time,
            }, timeout=timedelta(days=1).total_seconds())
            return True

        # If authenticated user exceeds the limit, send an email notification
        if user and user.is_authenticated and cache_value['count'] >= self.RATE_LIMITS['authenticated']:
            self.send_limit_exceeded_email(user)

        # If exceeded the rate limit, throttle the request
        raise Throttled(detail=f"Rate limit exceeded: {rate_limit} requests per day.")

    def send_limit_exceeded_email(self, user):
        """Send email notification to the subscriber when an authenticated user exceeds limit."""
        subscriber = Subscription.objects.filter(user=user).first()
        if subscriber:
            # Send an email to the subscriber (or admin) notifying them about the user exceeding their limit
            subject = 'Rate Limit Exceeded'
            message = f'The user {user.username} has exceeded the daily request limit.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [subscriber.user.email]  # or an admin's email
            send_mail(subject, message, email_from, recipient_list)
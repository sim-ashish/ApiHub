from django.contrib.auth.signals import user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from frontend.tasks import welcome_mail, security_mail

from django.core.mail import send_mail


@receiver(post_save, sender = User)
def user_created(sender, instance, created, **kwargs):
    if created:
        welcome_mail.delay('krushanuinfolabz@gmail.com', instance.email)



@receiver(user_login_failed)
def login_tried(sender, credentials, request, **kwargs):
    user = User.objects.filter(username = credentials['username']).first()
    if user:
        user_email = user.email
        security_mail.delay('krushanuinfolabz@gmail.com', user_email)
    
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_redis import get_redis_connection


@shared_task
def subscription_mail(sender_mail, to_mail, uId):
    html_content = render_to_string('frontend/email.html', {'link' : f'http://127.0.0.1:8000/subscribe/{uId}'})
    text_content = strip_tags(html_content)
    subject, from_email, to = 'Limit Exceeded', sender_mail, to_mail
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()



########### Redis TO Databse id transfer Schedules task #########################

def redis_task():
        # Connect to Redis
        r = get_redis_connection("default")

        # Define the key prefix
        key_prefix = 'your_prefix:*'

        # Initialize the cursor
        cursor = 0

        # List to store the keys
        keys = []

        # Iterate through the keys
        while True:
            cursor, new_keys = r.scan(cursor=cursor, match=key_prefix)
            keys.extend(new_keys)
            if cursor == 0:
                break

        # Fetch all the data for the keys
        data = {key: r.get(key) for key in keys}

        print(data)


        '''Start
        r = get_redis_connection("default")
        key_prefix = ':1:demo1*'
        cursor = 0

        # List to store the keys
        keys = []

        # Iterate through the keys
        while True:
            cursor, new_keys = r.scan(cursor=cursor, match=key_prefix)
            keys.extend(new_keys)
            if cursor == 0:
                break

        # Fetch all the data for the keys
        data = {key: r.get(key) for key in keys}
        li = list(data.keys())
        # print("Redis KEYYYYY : ",li[0].decode('utf-8'))   This will work
        # print("Redis KEYYYYY : ",data.decode('utf-8'))   not work 

        End'''
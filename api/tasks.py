from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_redis import get_redis_connection
import csv
from api.models import Request_logs
from django.utils import timezone
import os
from openpyxl import load_workbook
from django.conf import settings


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


############## Logging File Generator ##########################

@shared_task
def generate_log():
    upto_date = timezone.now() - timezone.timedelta(days=10)
    filtered_data = Request_logs.objects.filter(request_time__lte=timezone.now())
    
    if filtered_data:
        new_data = filtered_data.values_list('req_user', 'req_method', 'endpoint', 'ip_address', 'request_time')
        
        # Convert request_time to string using strftime() after getting the data
        formatted_data = []
        for row in new_data:
            formatted_row = list(row)
            formatted_row[4] = formatted_row[4].strftime('%Y-%m-%d %H:%M:%S')  
            formatted_data.append(tuple(formatted_row))
        
        # excel_file =os.path.join(settings.EXCEL_PATH, 'Logging.xlsx')
        # wb = load_workbook(excel_file)
        # ws = wb.active
        
        # for row in formatted_data:
        #     ws.append(row)
        
        # wb.save(excel_file)
        # filtered_data.delete()

        csv_file_path = os.path.join(settings.EXCEL_PATH, 'Logging.csv')
        with open(csv_file_path, mode='a', newline='') as file:
            # Create a csv.writer object
            writer = csv.writer(file)
            # Write data to the CSV file
            writer.writerows(formatted_data)
            filtered_data.delete()
    
    return "Log file Generated"



from celery import shared_task
from django.core.mail import EmailMultiAlternatives

@shared_task
def subscription_mail(sender_mail, to_mail):
    subject, from_email, to = 'Limit Exceed', sender_mail, to_mail
    text_content = 'Your Api Limit Exceeded'
    html_content = html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subscription</title>
    <style>
        *{{
            margin: 0;
            padding: 0;
        }}
        .container{{
            width: 60%;
            margin: auto;
        }}
        h1{{
            text-align: center;
            font-size: 6vw;
            margin-bottom: 5vh;
        }}
        p{{
            font-size: 1vw;
        }}
        @media only screen and (max-width: 800px) {{
            .container{{
                width: 80%;
                margin: auto;
            }}
            p{{
                font-size: 2.5vw;
            }}
        }}
        @media only screen and (max-width: 600px) {{
            .container{{
                width: 98%;
                margin: auto;
            }}
            p{{
                font-size: 2.5vw;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Limit Exceeded</h1>
        <p>Your Daily Limit for API hits has been consumed. You can access more tomorrow, or to get more hits, buy our subscription from the link below:<br>
        <a href="http://127.0.0.1:8000/subscribe/1">Buy Subscription</a>
        </p>
    </div>
</body>
</html>'''

    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



# @shared_task(name='Welcome-Mail')
# def welcome_mail(sender_mail, to_mail):
#     subject, from_email, to = 'Welcome', sender_mail, to_mail
#     text_content = 'This is an important message.'
#     html_content = '''<!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Welcome to ApiHub</title>
#             <style>
#                 *{
#                     margin: 0;
#                     padding: 0;
#                 }
#                 .container{
#                     width: 60%;
#                     margin: auto;
#                 }
#                 h1{
#                     text-align: center;
#                     font-size: 6vw;
#                     margin-bottom: 5vh;
#                 }
#                 p{
#                     font-size: 1vw;
#                 }
#                 @media only screen and (max-width: 800px) {
#                     .container{
#                     width: 80%;
#                     margin: auto;
#                 }
#                     p{
#                     font-size: 2.5vw;
#                 }
#                     }
#                     @media only screen and (max-width: 600px) {
#                     .container{
#                     width: 98%;
#                     margin: auto;
#                 }
#                     p{
#                     font-size: 2.5vw;
#                 }
#                     }

#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <h1>Welcome</h1>
#                 <p>Welcome to the ApiHub, Enjoy Real Api End-Points. Practice them in your learning, implement them in your Projects.
#                 <br>
#                 These are Secure End-points which uses JWt, so remember to get your JWT to access endpoints.
#                 </p>
#             </div>
            
#         </body>
#         </html>'''
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()

@shared_task(name='Welcome-Mail')
def welcome_mail(sender_mail, to_mail, link='http://127.0.0.1:8000'):
    html_content = render_to_string('frontend/email.html', {'link' : link})
    text_content = strip_tags(html_content)
    subject, from_email, to = 'Welcome to ApiHub', sender_mail, to_mail
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()


# @shared_task
# def security_mail(sender_mail, to_mail):
#     subject, from_email, to = 'Welcome', sender_mail, to_mail
#     text_content = 'This is an important message.'
#     html_content = '''<!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Welcome to ApiHub</title>
#             <style>
#                 *{
#                     margin: 0;
#                     padding: 0;
#                 }
#                 .container{
#                     width: 60%;
#                     margin: auto;
#                 }
#                 h1{
#                     text-align: center;
#                     font-size: 6vw;
#                     margin-bottom: 5vh;
#                 }
#                 p{
#                     font-size: 1vw;
#                 }
#                 @media only screen and (max-width: 800px) {
#                     .container{
#                     width: 80%;
#                     margin: auto;
#                 }
#                     p{
#                     font-size: 2.5vw;
#                 }
#                     }
#                     @media only screen and (max-width: 600px) {
#                     .container{
#                     width: 98%;
#                     margin: auto;
#                 }
#                     p{
#                     font-size: 2.5vw;
#                 }
#                     }

#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <h1>Security Alert!!</h1>
#                 <p>Someone Tries to login in our Website using your Username, we suggest you to change your password as soon as possible!
#                 </p>
#             </div>
            
#         </body>
#         </html>'''
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()


@shared_task
def security_mail(sender_mail, to_mail, link = 'http://127.0.0.1:8000'):
    html_content = render_to_string('frontend/security.html', {'link' : link})
    text_content = html_content
    subject, from_email, to = 'Security Alert', sender_mail, to_mail
    msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
    msg.content_subtype = "html"
    msg.attach_alternative(html_content, "text/html")
    msg.send()
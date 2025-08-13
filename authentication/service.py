from django.core.mail import send_mail
from django.conf import settings
import random
import string
from datetime import timedelta
from django.utils.timezone import now
from authentication.models import *

import base64

# def get_image_path(image_name):
#     # Construct the full path to the static file
#     image_path = settings.BASE_DIR / 'static' / 'images' / image_name
#     print(image_path)
#     return image_path

# def get_image_as_base64(image_path):
#     # Read the image file in binary mode and encode to base64
#     with open(image_path, "rb") as img_file:
#         encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
#     return encoded_string

def send_otp_email(staff_email, staff_name, system_name, otp_code):
    subject = 'Your Verification Code'
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #0047ab;
                color: #ffffff;
                padding: 20px;
                text-align: center;
                font-size: 20px;
            }}
            .content {{
                padding: 20px;
                text-align: left;
            }}
            .otp {{
                display: block;
                font-size: 30px;
                font-weight: bold;
                color: #219ad3;
                text-align: center;
                margin: 20px 0;
            }}
            .footer {{
                background-color: #f4f4f4;
                text-align: center;
                padding: 10px;
                font-size: 12px;
                color: #777777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{system_name}</h1>
                <h1>OTP Verification</h1>
            </div>
            <div class="content">
                <p>Dear {staff_name},</p>
                <p>You recently attempted to log in to <strong>{system_name}</strong>. To proceed, please use the following OTP code:</p>
                <div class="otp">{otp_code}</div>
                <p>This code will expire in <strong>2.5 minutes</strong>. Please do not share this code with anyone for security reasons.</p>
                <p>If you did not initiate this request, please report it to the IT support team immediately.</p>
            </div>
            <div class="footer">
                <p>Thank you,<br>PBZ BANK IT Support</p>
                <p>The People's Bank, The People's Choice</p>
            </div>
        </div>
    </body>
    </html>"""    
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, "", from_email, [staff_email], html_message=html_message)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False



def send_html_email(email, subject, message):  
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, "", from_email, [email], html_message=message)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

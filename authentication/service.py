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
    subject = "Your Verification Code"
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #2c3e50;
                background-color: #f8fafc;
                margin: 0;
                padding: 0;
                -webkit-font-smoothing: antialiased;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                border: 1px solid #e2e8f0;
            }}
            .header {{
                background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
                color: #ffffff;
                padding: 30px 20px;
                text-align: center;
                border-bottom: 4px solid #10b981; /* Financial Brand Accent Green */
            }}
            .header h1 {{
                margin: 0;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: #94a3b8;
            }}
            .header h2 {{
                margin: 5px 0 0 0;
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
            }}
            .content {{
                padding: 40px 35px;
                background-color: #ffffff;
            }}
            .content p {{
                margin: 0 0 16px 0;
                font-size: 15px;
                color: #334155;
            }}
            .otp-container {{
                background-color: #f0fdf4; /* Light green background badge */
                border: 1px dashed #10b981; /* Vibrant Green Border */
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                margin: 30px 0;
            }}
            .otp {{
                display: block;
                font-family: 'Courier New', Courier, monospace;
                font-size: 36px;
                font-weight: bold;
                color: #059669; /* Rich Premium Green */
                letter-spacing: 4px;
            }}
            .warning {{
                font-size: 13px !important;
                color: #64748b;
                background-color: #f8fafc;
                padding: 12px;
                border-radius: 6px;
                border-left: 3px solid #cbd5e1;
            }}
            .footer {{
                background-color: #f1f5f9;
                text-align: center;
                padding: 25px 20px;
                font-size: 12px;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
            }}
            .footer p {{
                margin: 4px 0;
            }}
            .tagline {{
                color: #1e3a8a; /* Brand Blue */
                font-weight: 600;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 8px !important;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{system_name}</h1>
                <h2>Security Verification</h2>
            </div>
            <div class="content">
                <p>Dear {staff_name},</p>
                <p>You recently attempted to log in to <strong>{system_name}</strong>. To proceed safely, please use the following One-Time Password (OTP):</p>
                
                <div class="otp-container">
                    <span class="otp">{otp_code}</span>
                </div>
                
                <p>This code will expire in <strong style="color: #0f172a;">3 minutes</strong>. For security reasons, do not share this code with anyone.</p>
                <p class="warning"><strong>Notice:</strong> If you did not initiate this security request, please change your credentials immediately and contact the IT security team.</p>
            </div>
            <div class="footer">
                <p>Thank you,<br><strong>PBZ BANK IT Support Team</strong></p>
                <p class="tagline">The People's Bank, The People's Choice</p>
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

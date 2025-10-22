from django.core.mail import EmailMessage
from django.conf import settings

def send_otp_email(email, otp):
    # print("TRying to send email")
    try:
        mail = EmailMessage(
            subject='Your OTP Verification Code',
            body=f'Your OTP is {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        mail.send(fail_silently=False)
    except Exception as e:
        print(f"[ERROR] Could not send OTP: {e}")

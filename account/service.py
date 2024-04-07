from .models import  MailVerificationOTP
import random


# to send mail
from django.core.mail import send_mail
from django.conf import settings





def send_otp_for_mail_verification(otp, user):
        send_mail(
                'Mail Verification',
                f'Hii  {user.username},\n\n\n\nYour OTP:   {otp}\n\nOTP will expire after 30 minutes.\n\nThankyou',
                settings.EMAIL_HOST_USER,
                [user.email], 
                fail_silently=True)
    
def get_otp_for_mail_verification(user):
      otp = random.randint(1001, 9999)

      if MailVerificationOTP.objects.filter(user = user.id).exists():
         otp_obj = MailVerificationOTP.objects.get(user = user.id)
         otp_obj.otp = otp
         otp_obj.save()

      else :  
        otp_obj = MailVerificationOTP(otp = otp, user = user)
        otp_obj.save()

      return otp

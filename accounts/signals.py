import random
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from config import settings
from djoser.signals import user_registered, user_activated
from .models import ActivationOtp
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created


User = get_user_model()
site_name = "MyKontainer"
url="mykontainer.app"


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance,reset_password_token, *args, **kwargs):
    
    token = reset_password_token.key
    user = reset_password_token.user

    if user.is_admin:
        token_url = f"https://admin.mykontainer.app/confirm-password/{token}"
    else:
        token_url = f"https://dashboard.mykontainer.app/reset-password/{token}"
    
    msg_html = render_to_string('email/password_reset.html', {
                        "token_url":token_url,
                        'url':url,
                        "user":user})
    
    message= 'Hello {},\n\nYou are receiving this message because you or someone else have requested the reset of the password for your account.\nClick on  the below to reset password:\n{}\n\nIf you did not request this please ignore this e-mail and your password would remain unchanged. \n\nRegards,\nMykontainer Support'.format(user.first_name, token_url)
    
    send_mail(
        subject = "RESET PASSWORD FOR MYKONTAINER",
        message= message,
        html_message=msg_html,
        from_email  = 'MyKontainer Support<noreply@mykontainer.app>',
        
        recipient_list= [user.email]
    )
    

def generate_otp(n):
    return "".join([str(random.choice(range(10))) for _ in range(n)])


@receiver(post_save, sender=User)
def send_details(sender, instance, created, **kwargs):
    if created and instance.is_superuser!=True and instance.is_admin==True:
        # print(instance.password)
        role = " ".join(str(instance.role).split('_'))
        subject = f"YOUR {role} ACCOUNT FOR MYKONTAINER".upper()
        
        message = f"""Hi, {str(instance.first_name).title()}.
You have just been onboarded on the MyKontainer platform. Your login details are below:
E-mail: {instance.email} 
password: {instance.password}    

Cheers,
MyKontainer Team   
"""   
        # msg_html = render_to_string('signup_email.html', {
        #                 'first_name': str(instance.first_name).title(),
        #                 'code':code,
        #                 'url':url})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail( subject, message, email_from, recipient_list)
        
        instance.set_password(instance.password)
        instance.save()
        # print(instance.password)
        return
    

@receiver(user_registered)
def activate_otp(user, request, *args,**kwargs):
    user.is_active = False
    user.save()
    
    code = generate_otp(6)
    expiry_date = timezone.now() + timezone.timedelta(minutes=10)
    ActivationOtp.objects.create(code=code, expiry_date=expiry_date, user=user)
    
    
    subject = "ACCOUNT VERIFICATION FOR MYKONTAINER"
        
    message = f"""Hi, {str(user.first_name).title()}.
Thank you for signing up!
Complete your verification on the {site_name} with the OTP below:

                {code}        

Expires in 5 minutes!

Cheers,
{site_name} Team            
"""   
    msg_html = render_to_string('email/activation.html', {
                    'first_name': str(user.first_name).title(),
                    'code':code,
                    'site_name':site_name,
                    "url":url})
    
    email_from = settings.Common.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
    
    return


@receiver(user_activated)
def comfirmaion_email(user, request, *args,**kwargs):
    
    
    subject = "VERIFICATION COMPLETE"
        
    message = f"""Hi, {str(user.first_name).title()}.
Your account has been activated and is ready to use!

Cheers,
{site_name} Team            
"""   
    msg_html = render_to_string('email/confirmation.html', {
                    'first_name': str(user.first_name).title(),
                    'site_name':site_name,
                    "url":url})
    
    email_from = settings.Common.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
    
    return
        
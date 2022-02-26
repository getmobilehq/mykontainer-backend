from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from config import settings

User = get_user_model()

@receiver(post_save, sender=User)
def send_details(sender, instance, created, **kwargs):
    if created and instance.is_superuser!=True:
        # print(instance.password)
        subject = f"YOUR {instance.role} ACCOUNT FOR MYKONTAINER".upper()
        
        message = f"""Hi, {str(instance.first_name).title()}.
You have just been onboarded on the quicksos platform. Your login details are below:
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
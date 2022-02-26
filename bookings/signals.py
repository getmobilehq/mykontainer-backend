from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from config import settings
from .models import Booking

@receiver(post_save, sender=Booking)
def send_notice(sender, instance, created, **kwargs):
    if created:
        # print(instance.password)
        subject = f"YOU MADE A NEW BOOKING".upper()
        
        message = f"""Hi, {str(instance.user.first_name).title()}.
You just made a new booking on the mykontainer platform. Kindly proceed to the bay area to drop the designated container. Your drop off code is given below.

Drop off code: {instance.drop_off}  
Location: {instance.bay_area.address}  

Cheers,
MyKontainer Team  
"""   
        # msg_html = render_to_string('signup_email.html', {
        #                 'first_name': str(instance.first_name).title(),
        #                 'code':code,
        #                 'url':url})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]
        send_mail( subject, message, email_from, recipient_list)
        
       
        return
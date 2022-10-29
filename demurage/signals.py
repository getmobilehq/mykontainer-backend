from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from config import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import DemurrageCalculations


@receiver(post_save, sender=DemurrageCalculations)
def send_details(sender, instance, created, **kwargs):
    if created:
        # print(instance.password)
        subject = f"Your Demurage Calculation on MyKontainer App"
        
        message = f"""Hello!
See the results of your Demurage Calculation on the MyKontainer Platform:

Container Type: {instance.container_type}
Start Date: {instance.start_date}
End Date  : {instance.end_date}
Chargeable days : {instance.chargeable_days}
Free days : {instance.free_days}
Amount" : {instance.amount}
VAT     : {instance.vat_amount},
Total   : {instance.total}
Currency: {instance.currency}

Cheers,
MyKontainer Team   
"""   
        # msg_html = render_to_string('signup_email.html', {
        #                 'first_name': str(instance.first_name).title(),
        #                 'code':code,
        #                 'url':url})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        try:
            send_mail( subject, message, email_from, recipient_list)
            
        except Exception as e:
            return
        
     
        # print(instance.password)
        return
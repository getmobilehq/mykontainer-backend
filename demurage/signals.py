from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from config import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import DemurrageCalculations
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import os

site_name = "MyKontainer"
url="mykontainer.app"

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
        msg_html = render_to_string('calculator_invoice.html', {
                        'container_type': instance.container_type,
                        'start_date':instance.start_date,
                        'end_date':instance.end_date,
                        "chargeable_days":instance.chargeable_days,
                        'free_days':instance.free_days,
                        'amount':instance.amount,
                        'vat_amount':instance.vat_amount,
                        'total':instance.total,
                        'currency':instance.currency,
                        "site_name":site_name,
                        "url":url,
                        "shipping_line":instance.shipping_company.name})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        
        try:
            send_mail( subject, message, email_from, recipient_list,html_message=msg_html)
            
        except Exception as e:
            return
        
     
        
        #### Add email to mailchimp

        mailchimp = Client()
        mailchimp.set_config({
        "api_key": os.getenv("MAILCHIMP_KEY"),
        "server": "us8"
        })

        list_id = os.getenv("LIST_ID")

        member_info = {
            "email_address": instance.email,
            "status_if_new": "subscribed",
        }

        try:
            
            response = mailchimp.lists.set_list_member(list_id, member_info.get("email_address").lower(), member_info)

            
        except ApiClientError as error:
            error_data = eval(error.text)
            
            send_mail(subject="Error Adding Email to MailChimp",
                      message =f"""Hello, Administrator.
The API was unable to add {instance.email} to the mailchimp account. It failed with the following error:
{error_data}
                      
Cheers,
MyKontainer Support""", 
            email_from = "MyKontainer Support <noreply@mykontainer.app>", 
            recipient_list=["mykontainertech@gmail.com"])
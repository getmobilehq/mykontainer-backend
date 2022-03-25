from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BayArea
from config.settings import Common

User = get_user_model()

@receiver(post_save, sender=BayArea)
def send_details(sender, instance, created, **kwargs):
    instance:BayArea
    
    if instance.available_space <=instance.threshold:
                    admins = [admin[0] for admin in User.objects.filter(role="admin").values_list("email")]
                    send_mail(
                        subject="THRESHOLD REACHED: Immediate action required!",
                        message=f"""Hello,
The bay with the name {instance.name} for shipping company with the name {instance.shipping_company.name} has gotten to it's threshold. 
Kindly reach out to the holding bay admin to update the available space information for this bay area.

Regards,
MyKontainer Support.""",
                    recipient_list=admins,
                    from_email= Common.DEFAULT_FROM_EMAIL
                )
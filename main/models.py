from django.db import models
import uuid
from django.forms import model_to_dict
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


# User = get_user_model()
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")

class ShippingCompany(models.Model):
    id    = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name  = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 20, validators=[phone_regex])
    opening_hours = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active= models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Shipping company')
        verbose_name_plural = _('Shipping companies')
        
        
    def __str__(self) -> str:
        return self.name
    
    
    def delete(self):
        self.is_active=False
        self.save()
        self.bookings.update(is_active=False)
        self.shipping_admins.update(is_active=False)
        self.demurages.update(is_active=False)
        for bay in self.bay_areas.all():
            bay.delete()
        return 
    
class BayArea(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 20, validators=[phone_regex])
    shipping_company = models.ForeignKey(ShippingCompany, related_name="bay_areas", on_delete=models.CASCADE)
    available_space = models.IntegerField(default=0)
    threshold = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active= models.BooleanField(default=True)
    
    
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def shipping_company_detail(self):
        return model_to_dict(self.shipping_company)
        
    def delete(self):
        self.is_active=False
        self.save()
        self.bookings.update(is_active=False)
        self.bay_admins.update(is_active=False)
        return 
    
    

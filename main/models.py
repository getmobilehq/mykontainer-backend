from django.db import models
import uuid
from django.forms import model_to_dict
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth import get_user_model


# User = get_user_model()

class ShippingCompany(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
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
        return 
    
    
class BayArea(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=500)
    shipping_company = models.ForeignKey(ShippingCompany, related_name="bay_areas", on_delete=models.CASCADE)
    available_space = models.IntegerField(default=0)
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
        return 
    
    

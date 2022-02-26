from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from main.models import ShippingCompany, BayArea


User = get_user_model()

# Create your models here.
class Booking(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed")
    )
      
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE, null=True)
    shipping_company = models.ForeignKey(ShippingCompany, related_name="bookings", on_delete=models.CASCADE)
    bay_area =  models.ForeignKey(BayArea, related_name="bookings", on_delete=models.CASCADE)
    date = models.DateField()
    laden_number = models.CharField(max_length=350)
    container_number = models.CharField(max_length=350)
    container_size = models.CharField(max_length=350)
    drop_off = models.CharField(max_length=6, null=True, blank=True)
    status = models.CharField(max_length=50, default="pending", choices=STATUS)
    is_active= models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def shipping_company_detail(self):
        return model_to_dict(self.shipping_company)
    
    @property
    def bay_area_detail(self):
        return model_to_dict(self.bay_area)
        
        
    def delete(self):
        self.is_active=False
        self.save()
        
    def __str__(self) -> str:
        return f"Booking for {self.bay_area.name}"
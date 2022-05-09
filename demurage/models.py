import uuid
from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Demurage(models.Model):
    SIZES = [("20 feet", "20 feet"),
               ("40 feet", "40 feet")]
    
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    shipping_company = models.ForeignKey("main.ShippingCompany", on_delete=models.CASCADE, related_name="demurages")
    start_day = models.IntegerField()
    end_day = models.IntegerField()
    price_per_day = models.FloatField()
    size = models.CharField(max_length=255, choices=SIZES)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
        
    
    @property
    def shipping_company_detail(self):
        return model_to_dict(self.shipping_company, exclude=["date_added","is_active"])
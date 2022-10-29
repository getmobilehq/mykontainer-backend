import uuid
from django.db import models
from django.forms import model_to_dict

# Create your models here.

class DemurageSize(models.Model):
    # SIZES = (('Dry 20 ft', 'Dry 20 ft'),
    #          ('Reefer 20 ft', 'Reefer 20 ft'),
    #          ('Special 20 ft', 'Special 20 ft'),
    #          ('Dry 40 ft', 'Dry 40 ft'),
    #          ('Reefer 40 ft', 'Reefer 40 ft'),
    #          ("Special 40 ft", "Special 40 ft"),
    #          ("Dry 45 ft", "Dry 45 ft"),
    #          ("Reefer 45 ft", "Reefer 45 ft"))
		
		

    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    shipping_company = models.ForeignKey("main.ShippingCompany", on_delete=models.CASCADE, null=True, blank=True, related_name="demurage_size")
    container_type = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    free_days = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    @property
    def shipping_company_detail(self):
        return model_to_dict(self.shipping_company, exclude=["date_added","is_active"])
        
    def delete(self):
        self.is_active=False
        self.ranges.update(is_active=False)
        self.save()
        
    def __str__(self):
        return f"{self.container_type} {self.size}"
        
        

class Demurage(models.Model):
    
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    shipping_company = models.ForeignKey("main.ShippingCompany", on_delete=models.CASCADE, related_name="demurages")
    start_day = models.IntegerField()
    end_day = models.IntegerField()
    price_per_day = models.FloatField()
    size = models.ForeignKey("demurage.DemurageSize", on_delete=models.CASCADE, related_name="ranges", null=True)
    demurage_type = models.CharField(max_length=250, blank=True, null=True, choices=(("import", "Import"),
    ("export","Export")))
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
        
    
    @property
    def shipping_company_detail(self):
        return model_to_dict(self.shipping_company, exclude=["date_added","is_active"])
    
    
    @property
    def size_detail(self):
        return model_to_dict(self.size, exclude=["date_added","is_active"])
    
    
    
class DemurrageCalculations(models.Model):
    email = models.EmailField()
    container_type= models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    chargeable_days = models.IntegerField(default=0)
    free_days = models.IntegerField()
    amount = models.FloatField()
    vat_amount = models.FloatField()
    total = models.FloatField()
    currency = models.CharField(max_length=5, default= "NGN")
    is_active= models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def delete(self):
        self.is_active=False
        self.save()
    
    def __str__(self):
        return f"{self.email} -- {self.date_created}"
    
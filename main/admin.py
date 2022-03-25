from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register([ShippingCompany, BayArea])


@admin.register(ShippingCompany)
class ShippingCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', "name", "is_active"]
    list_editable = ("is_active",)
    
@admin.register(BayArea)
class BayAreaAdmin(admin.ModelAdmin):
    list_display = ['id', "name", "is_active"]
    list_editable = ("is_active",)
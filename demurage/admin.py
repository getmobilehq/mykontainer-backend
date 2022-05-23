from django.contrib import admin
from .models import Demurage, DemurageSize
# Register your models here.

admin.site.register(DemurageSize)

@admin.register(Demurage)
class DemurageAdmin(admin.ModelAdmin):
    list_display = ['id', "shipping_company","is_active"]
    list_editable = ("is_active",)
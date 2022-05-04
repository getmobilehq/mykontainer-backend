from django.contrib import admin
from .models import Demurage
# Register your models here.


@admin.register(Demurage)
class DemurageAdmin(admin.ModelAdmin):
    list_display = ['id', "shipping_company", "size","is_active"]
    list_editable = ("is_active",)
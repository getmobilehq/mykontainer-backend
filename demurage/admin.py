from django.contrib import admin
from .models import Demurage, DemurageSize
# Register your models here.

admin.site.register(DemurageSize)

@admin.register(Demurage)
class DemurageAdmin(admin.ModelAdmin):
    list_display = ['id', "size","start_day","end_day","price_per_day", "demurage_type","shipping_company","is_active"]
    list_filter = ["shipping_company"]
    list_editable = ("is_active","price_per_day")
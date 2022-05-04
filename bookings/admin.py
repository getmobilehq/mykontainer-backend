from django.contrib import admin
from . models import Booking

# Register your models here.
# admin.site.register(Booking)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', "user", "is_active"]
    list_editable = ("is_active",)
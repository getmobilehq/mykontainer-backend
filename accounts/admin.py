from django.contrib import admin
from accounts.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "role", "is_active", "is_admin"]
    list_editable = ["role", "is_active", "is_admin"]
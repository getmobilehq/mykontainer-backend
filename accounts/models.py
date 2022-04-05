from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone

from main.models import BayArea, ShippingCompany

from .managers import UserManager
import uuid



class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('bay_admin', 'Bay Admin'),
        ('shipping_admin', 'Shipping Admin'),
        ('user', 'User')
    )    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+2341234567890'. Up to 15 digits allowed.")
    
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    first_name    = models.CharField(_('first name'),max_length = 250)
    last_name     = models.CharField(_('last name'),max_length = 250)
    role          = models.CharField(_('role'), max_length = 250, choices=ROLE_CHOICES)
    email         = models.EmailField(_('email'), unique=True)
    phone         = models.CharField(_('phone'), max_length = 20, unique = True, validators=[phone_regex])
    user_type = models.CharField(_("user type"), max_length=300, null=True, blank=True)
    company_name = models.CharField(_("company name"), max_length=300, null=True, blank=True)
    address       = models.CharField(_('address'), max_length = 250, null = True)
    password      = models.CharField(_('password'), max_length=300)
    shipping_company = models.ForeignKey(
        to=ShippingCompany,
        on_delete=models.CASCADE, 
        related_name="shipping_admins", 
        null=True)
    bay_area = models.ForeignKey(
        to=BayArea,
        on_delete=models.CASCADE, 
        related_name="bay_admins", 
        null=True)
    is_staff      = models.BooleanField(_('staff'), default=False)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 
                       'last_name', 
                       'phone', 
                       'address',
                       'role',
                       'shipping_company',
                       'bay_area',
                       'company_name',
                       'user_type'
                       ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.email} -- {self.role}"
    
    def delete(self):
        self.is_active = False
        self.save()
        
        
        
class ActivationOtp(models.Model):
    user  =models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expiry_date = models.DateTimeField()
    
    
    def is_valid(self):
        return bool(self.expiry_date > timezone.now())



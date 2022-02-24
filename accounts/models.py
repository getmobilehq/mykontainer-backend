from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

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
    role          = models.CharField(_('role'),max_length = 250, choices=ROLE_CHOICES)
    email         = models.EmailField(_('email'), unique=True)
    business_name = models.CharField(_('business name'),max_length = 250, null=True)
    phone         = models.CharField(_('phone'), max_length = 20, unique = True, validators=[phone_regex])
    address       = models.CharField(_('address'), max_length = 250, null = True)
    password      = models.CharField(_('password'), max_length=300)
    is_staff      = models.BooleanField(_('staff'), default=False)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 
                       'last_name', 
                       'business_name',
                       'phone', 
                       'address',
                       'role',
                       ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
    
    def delete(self):
        self.is_active = False
        self.save()


from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^09[0|1|2|3][0-9]{8}$', message='لطفا شماره موبایل خود را به درستی وارد کنید')
    phone = models.CharField(max_length=11, validators=[phone_regex], unique=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    logged_in = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/users', default='images/users/user.jpg')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.phone

    @property
    def full_name(self):
        if self.name != '':
            return self.name
        else:
            return self.phone


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^09[0|1|2|3][0-9]{8}$', message='لطفا شماره موبایل خود را به درستی وارد کنید')
    phone = models.CharField(max_length=11, null=False, blank=False, validators=[phone_regex,], unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    expire_at = models.DateTimeField(blank=True)
    resend_at = models.DateTimeField(blank=True)
    count = models.IntegerField(default=1)
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
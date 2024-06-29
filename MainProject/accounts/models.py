from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django_jalali.db import models as jmodel
from utils.baseModel import BaseModel

from accounts.manager import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    birthday = models.CharField(max_length=10,null=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    object = UserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return 'کاربر عزیز'


class Otp(BaseModel):
    code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=12)


class Address(BaseModel):
    user = models.ForeignKey('User', models.CASCADE, 'user_address')
    neighbourhood = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    formatted_address = models.TextField()
    plaqe = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.state}-{self.formatted_address}-{self.plaqe}-{self.floor}-{self.postal_code}'




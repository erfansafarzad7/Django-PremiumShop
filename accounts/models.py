from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from .validators import phone_number_validation
from orders.models import Cart
import random


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=40, null=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=11, validators=[phone_number_validation, ], unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', ]

    objects = UserManager()

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_otp')
    code = models.CharField(max_length=5, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.user.phone_number} - {self.code}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        random_code = random.randint(10000, 99999)
        OTP.objects.create(user=instance, code=random_code)
        Cart.objects.create(user=instance)

        if instance.phone_number:
            # send sms
            print(random_code)
        if instance.email:
            # send email
            print(random_code)


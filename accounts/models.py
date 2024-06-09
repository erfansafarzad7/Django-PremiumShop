from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from .managers import UserManager
from .validators import phone_number_validation
from orders.models import Cart
import random


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('نام کاربری'), max_length=40, null=True, blank=True)
    email = models.EmailField(_('ایمیل'), unique=True)
    phone_number = models.CharField(_('شماره تلفن'), max_length=11, validators=[phone_number_validation, ], unique=True, null=True, blank=True)
    is_staff = models.BooleanField(_("ادمین"), default=False)
    is_active = models.BooleanField(_("فعال"), default=True)
    is_verified = models.BooleanField(_("تایید شده"), default=False)

    created_date = models.DateTimeField(_("تاریخ ثبتنام"), auto_now_add=True)
    updated_date = models.DateTimeField(_("تاریخ آپدیت"), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', ]

    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_otp', verbose_name="کاربر")
    code = models.CharField(_("کد یکبار مصرف"), max_length=5, unique=True)
    created_date = models.DateTimeField(_("تاریخ تولید"), auto_now_add=True)

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کد های یکبار مصرف'

    def __str__(self):
        return f'{self.user.email} - {self.user.phone_number} - {self.code}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        random_code = random.randint(10000, 99999)
        OTP.objects.create(user=instance, code=random_code)
        Cart.objects.create(user=instance)

        if instance.phone_number:
            # send sms                                         # <==================================================
            print(random_code)
        if instance.email:
            send_mail(
                "کد شما :",
                f"سلام . کد شما برای ورود به سایت : {random_code}",
                "efi.dragon20002gmail.com",
                [instance.email, ]
            )
            print(random_code)


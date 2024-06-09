from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from items.models import Item
import random


class Coupon(models.Model):
    code = models.CharField(_("تخفیف"), max_length=30, unique=True)
    discount_percent = models.PositiveSmallIntegerField(_("تخفیف"))

    created_date = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(_("تاریخ آپدیت"), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

    def __str__(self):
        return f"{self.code} - {self.discount_percent}"


STATUS_CHOICES = (
    ('تایید شده', _("تایید شده")),
    ('درحال پرداخت', _("درحال پرداخت")),
    ('درحال انجام', _("درحال انجام")),
    ('انجام شده', _("انجام شده")),
    ('لغو شده', _("لغو شده")),
)


class Order(models.Model):
    code = models.CharField(_("کد سفارش"), max_length=10, unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="user_order", verbose_name='کاربر')
    status = models.CharField(_("وضعیت سفارش"), max_length=15, choices=STATUS_CHOICES, default='تایید شده')
    items = models.ManyToManyField('items.Item', related_name='order_items', blank=True, verbose_name='آیتم ها')

    coupon_used = models.PositiveSmallIntegerField(_("درصد کد تخفیف استفاده شده"), default=0)
    must_pay = models.PositiveIntegerField(_("قابل پرداخت"), default=0)
    paid = models.PositiveIntegerField(_("مبلغ پرداخت شده"), default=0)

    created_date = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(_("تاریخ آپدیت"), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return self.code

    @property
    def calculate_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.discounted_price
        return int(total)


@receiver(post_save, sender=Order)
def create_profile(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "New Order :",
            f"{instance.user.email} - {instance.code}",
            "efi.dragon20002gmail.com",
            ["erfansafarzad7@gmail.com", ] # send email to admin
        )
    else:
        instance.status = 'Answered'
        send_mail(
            f"تیکت شما به {instance.status} تغییر پیدا کرد :",
            f"سفارش شما با کد ' {instance.code} ' به ' {instance.status} ' تغییر پیدا کرد. ",
            "efi.dragon20002gmail.com",
            [instance.user.email, ] # send email to user
        )


# class CartItem(models.Model):
#     item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField()
#     total_price = models.PositiveSmallIntegerField()
#
#     def __str__(self):
#         return f'{self.item} - {self.quantity}'


class Cart(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, verbose_name='کاربر')
    items = models.ManyToManyField('items.Item', related_name='cart_items', blank=True, verbose_name='آیتم ها')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name="cart_coupon", null=True, blank=True, verbose_name='کد تخفیف')

    created_date = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_date = models.DateTimeField(_("تاریخ آپدیت"), auto_now=True)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self):
        return f'{self.user} - {self.items.count()}'

    @property
    def count_items(self):
        return self.items.count()

    @property
    def calculate_total_price_with_discount(self):
        total = 0
        for item in self.items.all():
            total += item.discounted_price
        return int(total)

    @property
    def calculate_total_price_without_discount(self):
        total = 0
        for item in self.items.all():
            total += item.price
        return int(total)

    @property
    def calculate_total_discount(self):
        total = 0
        for item in self.items.all():
            total += item.discount
        return int(total / self.items.count())

    @property
    def calculate_total_price_with_coupon(self):
        total_price = int(self.calculate_total_price_with_discount)

        if coupon := self.coupon:
            return int(total_price * (1 - coupon.discount_percent / 100))

        return total_price

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from items.models import Item
import random


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveSmallIntegerField()

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}"


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('On Pay', 'On Pay'),
    ('In Progress', 'In Progress'),
    ('Done', 'Done'),
    ('Cancelled', 'Cancelled'),
)


class Order(models.Model):
    code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="user_order")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Accepted')
    items = models.ManyToManyField('items.Item', related_name='order_items', blank=True)

    coupon_used = models.PositiveSmallIntegerField(default=0)
    must_pay = models.PositiveSmallIntegerField(default=0)
    paid = models.PositiveSmallIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.code

    @property
    def calculate_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.discounted_price
        return int(total)

# class CartItem(models.Model):
#     item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField()
#     total_price = models.PositiveSmallIntegerField()
#
#     def __str__(self):
#         return f'{self.item} - {self.quantity}'


class Cart(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    items = models.ManyToManyField('items.Item', related_name='cart_items', blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, related_name="cart_coupon", null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

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
        return int(total)

    @property
    def calculate_total_price_with_coupon(self):
        total_price = int(self.calculate_total_price_with_discount)

        if coupon := self.coupon:
            return int(total_price * (1 - coupon.discount_percent / 100))

        return total_price

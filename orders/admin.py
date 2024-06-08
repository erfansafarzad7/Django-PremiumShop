from django.contrib import admin
from .models import Order, Cart, Coupon


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'calculate_total_price', 'status', 'created_date', 'updated_date')
    search_fields = ('code', 'items')
    list_filter = ('status', 'created_date', 'updated_date')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'count_items', 'created_date', 'updated_date')
    search_fields = ('user', )
    list_filter = ('created_date', 'updated_date')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'created_date', 'updated_date')
    search_fields = ('code', 'discount_percent')
    list_filter = ('created_date', 'updated_date')


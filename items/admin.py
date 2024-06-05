from django.contrib import admin
from .models import Item, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title', )
    list_filter = ('created_date', )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discount', 'discounted_price', 'created_date', 'updated_date')
    search_fields = ('title', 'category')
    list_filter = ('created_date', 'updated_date')


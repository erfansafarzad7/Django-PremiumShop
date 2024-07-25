from django.contrib import admin
from .models import Item, Category, Choices, Variables


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title', )
    list_filter = ('created_date', )


class ChoicesInline(admin.TabularInline):
    model = Choices.choices.through
    extra = 5


class ItemChoicesInline(admin.TabularInline):
    model = Item.choices.through
    extra = 2


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemChoicesInline, ]

    list_display = ('title', 'category', 'created_date', 'updated_date')
    search_fields = ('title', 'category')
    list_filter = ('created_date', 'updated_date')

    fieldsets = (
        (None, {
            'fields': ('image',)
        }),
        (None, {
            'fields': ('title', 'description', )
        }),
        (None, {
            'fields': ('category', )
        }),
    )


@admin.register(Choices)
class ChoicesAdmin(admin.ModelAdmin):
    inlines = [ChoicesInline, ]

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
    )


admin.site.register(Variables)

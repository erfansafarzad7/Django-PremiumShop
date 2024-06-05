from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status', 'created_date', 'updated_date')
    search_fields = ('user__email', 'title')
    list_filter = ('status', 'created_date', 'updated_date')

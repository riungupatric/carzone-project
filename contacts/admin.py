from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'phone',
                    'car_title', 'customer_need', 'created_date')
    search_fields = ('last_name', 'email', 'car_title')
    list_per_page = 25

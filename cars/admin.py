from django.contrib import admin
from .models import Car
from django.utils.html import format_html


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # car thumbnail
    def thumbnail(self, object):
        return format_html(f'<img src="{object.car_photo.url}" width="40px" >')
    list_display = ('thumbnail', 'car_title', 'color', 'engine',
                    'condition', 'milage', 'is_featured')

    list_display_links = ('car_title',)

    # make a column editable
    list_editable = ('is_featured',)

    # many search fields can strain the database
    search_fields = ('car_title', 'model', 'fuel_type', 'city', 'condition')

    list_filter = ('model', 'fuel_type', 'city')

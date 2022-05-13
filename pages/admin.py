from csv import list_dialects
from django.contrib import admin
from .models import Team
from django.utils.html import format_html


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    # display team member thumbnail
    def thumbnail(self, object):
        return format_html(f'<img src="{object.photo.url}" width="40" style="border-radius:45px" >')
    # change the name of the thumbnail column from thumbnail to photo
    thumbnail.short_description = 'photo'

    list_display = ('thumbnail', 'first_name', 'last_name',
                    'designation', 'created_date')

    # make first_name clickable
    list_display_links = ('first_name',)

    # serach field
    search_fields = ('last_name', 'designation')

    # filter
    list_filter = ('designation',)

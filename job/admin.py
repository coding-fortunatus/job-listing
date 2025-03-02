from django.contrib import admin
from .models import User
from django.utils.html import format_html


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'display_profile', 'resume')

    def display_profile(self, obj):
        if obj.profile:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile.url)
        return "No Image"

    display_profile.short_description = 'Profile'


admin.site.register(User, UserAdmin)

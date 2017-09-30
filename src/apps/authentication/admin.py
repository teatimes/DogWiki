from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.apps.authentication.models import User, Follow, Action


# Register your models here.
class UserAdmin(UserAdmin):
    model = User
    fieldset = (
        (None, {
            'fields': ('first_name', 'last_name', 'username', 'profile_image')
        })
    )

admin.site.register(User, UserAdmin)
admin.site.register(Follow)
admin.site.register(Action)
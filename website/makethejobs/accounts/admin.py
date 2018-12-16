from django.contrib import admin

# Register your models here.
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

admin.site.register(User, UserAdmin)
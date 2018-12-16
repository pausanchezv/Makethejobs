from django.contrib import admin

# Register your models here.
from accounts.models import User
from makethejobs.settings import PLATFORM_NAME


class UserAdmin(admin.ModelAdmin):
    """
    User Custom Admin
    """

    list_display = (
        'username',
        'headline',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'is_superuser',
        'is_staff',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'headline',
        'company',
    )

    def get_queryset(self, request):
        """
        Queryset order by
        """
        queryset = super(UserAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-pk')
        return queryset


# Customize titles
admin.site.site_header = '{} Database'.format(PLATFORM_NAME)
admin.site.site_title = '{} Database'.format(PLATFORM_NAME)

# Register models
admin.site.register(User, UserAdmin)

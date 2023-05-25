"""
Admin file admin portal.
"""
from django.contrib import admin
from .models import Strategy


class StrategyAdmin(admin.ModelAdmin):
    """Strategy configuration in admin portal."""

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            # Add any other fields you want to make read-only
            return 'user_id', 'id'
        return ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.using('secondary')  # Specify the secondary database
        return qs


admin.site.register(Strategy, StrategyAdmin)

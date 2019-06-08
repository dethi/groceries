from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, InboundEmail


@admin.register(InboundEmail)
class InboundEmailAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)

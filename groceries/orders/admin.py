from django.contrib import admin

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "delivery_date")


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    pass

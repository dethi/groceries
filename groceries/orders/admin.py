from django.contrib import admin

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("delivery_date", "shoppers_name", "origin")


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "unit_price", "total_price_pretty")

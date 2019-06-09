from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse


from . import models


class ItemInline(admin.TabularInline):
    model = models.Item


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("delivery_date", "shoppers_name", "pretty_price_per_shoppers")
    inlines = [ItemInline]


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "product",
        "quantity",
        "pretty_unit_price",
        "pretty_total_price",
        "pretty_price_per_shares",
    )

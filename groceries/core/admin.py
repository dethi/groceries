from dataclasses import asdict

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from groceries.orders.models import Order, Item

from .models import User, InboundEmail
from .services import parse_email


def process_email(modeladmin, request, queryset):
    for inbound_email in queryset:
        if hasattr(inbound_email, "order"):
            continue

        basket = parse_email(inbound_email.body_html)

        new_order = Order(origin=inbound_email)
        new_order.save()

        Item.objects.bulk_create(
            Item(order=new_order, **asdict(item)) for item in basket
        )


@admin.register(InboundEmail)
class InboundEmailAdmin(admin.ModelAdmin):
    list_display = ("pk", "sender", "recipient", "created_at", "updated_at")
    actions = [process_email]


admin.site.register(User, UserAdmin)

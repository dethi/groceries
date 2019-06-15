from collections import Counter

from django.db import models
from django.contrib.auth import get_user_model

from django_admin_display import admin_display

from .validators import validate_shares, parse_shares


class Order(models.Model):
    delivery_date = models.DateField(verbose_name="delivery date", auto_now_add=True)
    shoppers = models.ManyToManyField(get_user_model(), related_name="+", blank=True)
    origin = models.OneToOneField(
        "core.InboundEmail", on_delete=models.CASCADE, null=True
    )

    def shoppers_name(self):
        return [s.get_short_name() for s in self.shoppers.all()]

    def shoppers_initial(self):
        names = self.shoppers_name()
        initials = {name[0].lower() for name in names}
        if len(initials) != len(names):
            raise ValueError(f"Cannot create unique initials from {names}")
        return initials

    def price_per_shoppers(self):
        items = self.item_set.all()
        acc = Counter()
        for item in items:
            acc += Counter(item.price_per_share())
        return acc

    @admin_display(short_description="Shoppers Name")
    def pretty_shoppers_name(self):
        return ", ".join(self.shoppers_name())

    @admin_display(short_description="Price Per Shoppers")
    def pretty_price_per_shoppers(self):
        price_per_shoppers = self.price_per_shoppers()
        price_per_shoppers_str = ", ".join(
            f"{k}={round(v/100, 2)}€" for k, v in price_per_shoppers.items()
        )
        total = sum(price_per_shoppers.values())
        return f"{price_per_shoppers_str} total={round(total/100, 2)}€"

    def __str__(self):
        return f"Order {self.pk} - {self.delivery_date}"


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=140)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.IntegerField()
    shares = models.CharField(max_length=16, blank=True, validators=[validate_shares])

    def total_price(self):
        return self.quantity * self.unit_price

    def price_per_share(self):
        initials = set(self.order.shoppers_initial())
        if not initials:
            return {}
        if not self.shares:
            price_per_share = self.total_price() / len(initials)
            return {i: price_per_share for i in initials}

        parsed_shares = parse_shares(self.shares)
        total_shares = sum(parsed_shares.values())
        share_price = self.total_price() / total_shares
        return {k: v * share_price for k, v in parsed_shares.items()}

    @admin_display(short_description="Unit Price")
    def pretty_unit_price(self):
        return f"{round(self.unit_price / 100, 2)} €"

    @admin_display(short_description="Total Price")
    def pretty_total_price(self):
        return f"{round(self.total_price() / 100, 2)} €"

    @admin_display(short_description="Price Per Shares")
    def pretty_price_per_shares(self):
        return ", ".join(f"{k}={round(v/100), 2)}€" for k, v in self.price_per_share().items())

    def __str__(self):
        return f"Item {self.pk}"

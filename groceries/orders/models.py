from django.db import models
from django.contrib.auth import get_user_model


class Order(models.Model):
    delivery_date = models.DateField(verbose_name="delivery date", auto_now_add=True)
    shoppers = models.ManyToManyField(get_user_model(), related_name="+", blank=True)
    origin = models.OneToOneField(
        "core.InboundEmail", on_delete=models.CASCADE, null=True
    )

    def shoppers_name(self):
        return ", ".join(s.get_short_name() for s in self.shoppers.all())

    def __str__(self):
        return f"{self.pk} - {self.delivery_date}"


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=140)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.IntegerField()

    def total_price(self):
        return self.quantity * self.unit_price

    def total_price_pretty(self):
        return f"{self.total_price() / 100} €"

    total_price_pretty.short_description = "Total Price"


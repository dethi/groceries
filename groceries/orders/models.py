from django.db import models
from django.contrib.auth import get_user_model


class Order(models.Model):
    delivery_date = models.DateField(verbose_name="delivery date", auto_now_add=True)
    shoppers = models.ManyToManyField(get_user_model(), related_name="+")

    def __str__(self):
        return f"{self.pk} - {self.delivery_date}"


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=140)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.IntegerField()

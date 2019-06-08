from django.views.generic import ListView
from . import models

# Create your views here.
class OrderListView(ListView):
    model = models.Order

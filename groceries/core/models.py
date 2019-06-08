from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class InboundEmail(models.Model):
    sender = models.EmailField()
    recipient = models.EmailField()
    body_html = models.TextField()

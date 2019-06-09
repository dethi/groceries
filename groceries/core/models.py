from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class InboundEmail(models.Model):
    sender = models.EmailField()
    recipient = models.EmailField()
    body_html = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.pk} FROM {self.sender} TO {self.recipient}"

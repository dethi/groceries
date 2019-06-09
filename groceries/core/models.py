import quopri

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

import requests


class User(AbstractUser):
    pass


class InboundEmail(models.Model):
    sender = models.EmailField()
    recipient = models.EmailField()
    body_html = models.TextField()
    message_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def retrieve_message(self):
        if self.message_url is None:
            return

        # Retrieve email from Mailgun Messages API
        res = requests.get(self.message_url, auth=("api", settings.MAILGUN_API_KEY))
        res.raise_for_status()
        email = res.json()

        self.sender = email.get("sender")
        self.recipient = email.get("recipient")
        self.body_html = quopri.decodestring(email.get("stripped-html", "")).decode(
            "utf-8"
        )

    def __str__(self):
        return f"#{self.pk} FROM {self.sender} TO {self.recipient}"

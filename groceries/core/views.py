import quopri
import pprint

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import requests

from .models import InboundEmail


@csrf_exempt
def inbound_email_webhook(request):
    if request.method == "POST":
        pprint.pprint(request.POST)
        message_url = request.POST.get("message-url")

        email = InboundEmail(message_url=message_url)
        email.retrieve_message()
        email.save()

    return HttpResponse("OK")

from django.shortcuts import HttpResponse
from .models import InboundEmail


def inbound_email_webhook(request):
    if request.method == "POST":
        sender = request.POST.get("sender")
        recipient = request.POST.get("recipient")
        body_html = request.POST.get("body-html", "")

        email = InboundEmail(sender=sender, recipient=recipient, body_html=body_html)
        email.save()

    return HttpResponse("OK")

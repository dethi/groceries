from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import InboundEmail


@csrf_exempt
def inbound_email_webhook(request):
    if request.method == "POST":
        sender = request.POST.get("sender")
        recipient = request.POST.get("recipient")
        body_html = request.POST.get("body-html", "")

        email = InboundEmail(sender=sender, recipient=recipient, body_html=body_html)
        email.save()

    return HttpResponse("OK")


def redirect_to_admin(request):
    return redirect("admin:index", permanent=True)

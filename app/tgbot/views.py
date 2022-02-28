import json
import requests
from django.http import JsonResponse
from django.conf import settings
from .models import Recipient, Event


def send(request):
    data = json.loads(request.body)
    if not data.get('key') or data['key'] != settings.TGBOT_KEY:
        return JsonResponse({'ok': False})

    event = Event.objects.get(slug=data['event'])
    text = data['text']
    recipients = event.recipients.all()
    response = { "recipients": [] }

    for recipient in recipients:
        requests.post(settings.TELEGRAM_URL + 'sendMessage', data={ "chat_id": recipient.chat_id, "text": text })
        response["recipients"].append(recipient.username)

    return JsonResponse(response)
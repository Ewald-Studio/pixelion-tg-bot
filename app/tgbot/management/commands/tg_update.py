# -*- coding: utf-8 -*-
import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from tgbot.models import Recipient


class Command(BaseCommand):
    help = "Periodically update telegram state and get new subscribers"

    def handle(self, *args, **options):
        last_update_id = None

        while True:
            if last_update_id is None:
                request = requests.post(settings.TELEGRAM_URL + "getUpdates", data={ "allowed_updates": ["message"] })
            else:
                request = requests.post(settings.TELEGRAM_URL + "getUpdates", data={ "allowed_updates": ["message"], "offset": last_update_id + 1 })
            data = request.json()
            updates = data["result"]
            if len(updates) > 0:
                print (updates)
                last_update_id = updates[-1]["update_id"]
                self.create_recipients(updates)

            time.sleep(5)


    def create_recipients(self, updates):
        for update in updates:
            is_message = True
            try:
                chat = update["message"]["chat"]
            except:
                is_message = False
            
            if is_message:
                chat_id = chat["id"]
                recipient, created = Recipient.objects.get_or_create(chat_id=chat_id)
                if created:
                    print ("Created recipient: " + chat["username"])
                    recipient.first_name = chat["first_name"]
                    recipient.last_name = chat["last_name"]
                    recipient.username = chat["username"]
                    recipient.save()


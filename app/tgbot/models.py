from re import M
from django.db import models


class Event(models.Model):
    slug = models.SlugField(max_length=255)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Recipient(models.Model):
    chat_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    events = models.ManyToManyField(Event, related_name='recipients')

    def __str__(self):
        return f'@{self.username} — {self.first_name} {self.last_name}'

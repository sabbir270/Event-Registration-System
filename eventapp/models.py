
from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location_name = models.CharField(max_length=255)
    registered_users = models.ManyToManyField(User, related_name='registered_events', blank=True)

    def max_slots(self):
        return 5

    def available_slots(self):
        return self.max_slots() - self.registered_users.count()


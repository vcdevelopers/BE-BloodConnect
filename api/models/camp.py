from django.db import models
from datetime import date

class Camp(models.Model):
    name = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    zone = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=100)
    slots = models.IntegerField(default=100)
    slots_booked = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='upcoming')

    def save(self, *args, **kwargs):
        if self.date and self.date < date.today():
            self.status = 'completed'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} on {self.date} ({self.status})"

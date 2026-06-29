from django.db import models
from datetime import date, timedelta

class Donor(models.Model):
    name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=30)
    zone = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10)

    age = models.IntegerField()
    last_donation = models.DateField(null=True, blank=True)
    total_donations = models.IntegerField(default=0)
    eligible = models.BooleanField(default=True)
    next_eligible = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active')

    def save(self, *args, **kwargs):
        if self.last_donation:
            self.next_eligible = self.last_donation + timedelta(days=90)
            self.eligible = self.next_eligible <= date.today()
        else:
            self.eligible = True
            self.next_eligible = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.blood_group} ({self.zone})"

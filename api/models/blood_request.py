from django.db import models

class BloodRequest(models.Model):
    patient_name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=30)
    units = models.IntegerField(default=1)
    hospital = models.CharField(max_length=255)
    hospital_address = models.CharField(max_length=255, blank=True)
    attendant_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    urgency = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')
    date = models.DateField(auto_now_add=True)
    matched_donors_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Request for {self.patient_name} - {self.blood_group} ({self.urgency})"

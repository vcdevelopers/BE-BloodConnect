from django.db import models

class Campaign(models.Model):
    type = models.CharField(max_length=20)
    message = models.TextField()
    recipients = models.IntegerField(default=0)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    zone = models.CharField(max_length=100, blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')

    def __str__(self):
        return f"{self.type.upper()} Campaign on {self.sent_at.strftime('%Y-%m-%d %H:%M')}"

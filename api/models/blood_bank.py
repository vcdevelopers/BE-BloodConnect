from django.db import models

class BloodBank(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    zone = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=100, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    timestamp = models.CharField(max_length=100, blank=True)

    wb_a_pos = models.IntegerField(default=0)
    wb_a_neg = models.IntegerField(default=0)
    wb_b_pos = models.IntegerField(default=0)
    wb_b_neg = models.IntegerField(default=0)
    wb_ab_pos = models.IntegerField(default=0)
    wb_ab_neg = models.IntegerField(default=0)
    wb_o_pos = models.IntegerField(default=0)
    wb_o_neg = models.IntegerField(default=0)

    prbc_a_pos = models.IntegerField(default=0)
    prbc_a_neg = models.IntegerField(default=0)
    prbc_b_pos = models.IntegerField(default=0)
    prbc_b_neg = models.IntegerField(default=0)
    prbc_ab_pos = models.IntegerField(default=0)
    prbc_ab_neg = models.IntegerField(default=0)
    prbc_o_pos = models.IntegerField(default=0)
    prbc_o_neg = models.IntegerField(default=0)

    total_units = models.IntegerField(default=0)
    bombay_pos = models.IntegerField(default=0)
    bombay_neg = models.IntegerField(default=0)
    sd_platelets = models.IntegerField(default=0)
    sd_plasma = models.IntegerField(default=0)
    ffp = models.IntegerField(default=0)
    cryo_pp = models.IntegerField(default=0)
    liquid_plasma = models.IntegerField(default=0)
    rdp = models.IntegerField(default=0)
    cryo_pre = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.zone})"

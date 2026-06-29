from django.contrib import admin
from api.models.blood_bank import BloodBank
from api.models.blood_request import BloodRequest
from api.models.camp import Camp
from api.models.campaign import Campaign
from api.models.donor import Donor

@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'zone', 'district', 'contact', 'last_updated')
    search_fields = ('name', 'zone', 'district', 'pincode')
    list_filter = ('zone', 'district')

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'blood_group', 'units', 'hospital', 'hospital_address', 'urgency', 'status', 'date', 'matched_donors_count')
    search_fields = ('patient_name', 'hospital', 'hospital_address', 'phone')
    list_filter = ('blood_group', 'urgency', 'status', 'date')
    list_editable = ('status',)

@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organizer', 'zone', 'date', 'time', 'slots', 'slots_booked', 'status')
    search_fields = ('name', 'organizer', 'location', 'zone')
    list_filter = ('zone', 'date', 'status')
    list_editable = ('status',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'blood_group', 'zone', 'recipients', 'status', 'sent_at')
    search_fields = ('message', 'zone')
    list_filter = ('type', 'blood_group', 'zone', 'status')

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'blood_group', 'zone', 'phone', 'email', 'age', 'gender', 'eligible', 'status')
    search_fields = ('name', 'phone', 'email', 'zone')
    list_filter = ('blood_group', 'zone', 'eligible', 'status')
    list_editable = ('status', 'eligible')

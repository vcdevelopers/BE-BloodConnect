from rest_framework import serializers
from api.models import Donor

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'

    def to_internal_value(self, data):
        # Create a mutable copy of the dict if needed
        if hasattr(data, '_mutable'):
            data = data.copy()
        else:
            data = dict(data)

        # Support old frontend keys for robust caching mitigation
        if 'contact' in data and 'phone' not in data:
            data['phone'] = data['contact']
        if 'last_donation_date' in data and 'last_donation' not in data:
            data['last_donation'] = data['last_donation_date']

        return super().to_internal_value(data)

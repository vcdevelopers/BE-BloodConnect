from rest_framework import serializers
from api.models import BloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = '__all__'

    def to_internal_value(self, data):
        # Create a mutable copy of the dict if needed
        if hasattr(data, '_mutable'):
            data = data.copy()
        else:
            data = dict(data)

        # Support old frontend keys for robust caching mitigation
        if 'hospital_name' in data and 'hospital' not in data:
            data['hospital'] = data['hospital_name']
        if 'contact_person' in data and 'attendant_name' not in data:
            data['attendant_name'] = data['contact_person']
        if 'contact_number' in data and 'phone' not in data:
            data['phone'] = data['contact_number']
        if 'zone' in data and 'hospital_address' not in data:
            data['hospital_address'] = data['zone']

        return super().to_internal_value(data)

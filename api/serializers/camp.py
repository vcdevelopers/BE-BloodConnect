from rest_framework import serializers
from api.models import Camp

class CampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        fields = '__all__'

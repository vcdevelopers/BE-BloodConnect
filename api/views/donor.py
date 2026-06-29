from rest_framework import viewsets
from api.models import Donor
from api.serializers import DonorSerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all().order_by('-id')
    serializer_class = DonorSerializer

    def get_queryset(self):
        queryset = self.queryset.all()
        zone = self.request.query_params.get('zone', None)
        blood_group = self.request.query_params.get('blood_group', None)
        
        if zone:
            queryset = queryset.filter(zone__iexact=zone)
        if blood_group:
            queryset = queryset.filter(blood_group__iexact=blood_group)
        return queryset

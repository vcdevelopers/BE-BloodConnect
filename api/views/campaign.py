from rest_framework import viewsets
from api.models import Campaign
from api.serializers import CampaignSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('-sent_at')
    serializer_class = CampaignSerializer

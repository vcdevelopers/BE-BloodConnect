from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    BloodBankViewSet, DonorViewSet, BloodRequestViewSet, 
    CampViewSet, CampaignViewSet, StatsView
)

router = DefaultRouter()
router.register(r'bloodbanks', BloodBankViewSet, basename='bloodbank')
router.register(r'donors', DonorViewSet, basename='donor')
router.register(r'requests', BloodRequestViewSet, basename='request')
router.register(r'camps', CampViewSet, basename='camp')
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('stats/', StatsView.as_view(), name='stats'),
    path('', include(router.urls)),
]

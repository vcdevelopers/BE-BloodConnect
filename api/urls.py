from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    BloodBankViewSet, DonorViewSet, BloodRequestViewSet, 
    CampViewSet, CampaignViewSet, StatsView
)

from api.views.auth import LoginView, LogoutView, MeView
from api.views.broadcast import BroadcastView

router = DefaultRouter()
router.register(r'bloodbanks', BloodBankViewSet, basename='bloodbank')
router.register(r'donors', DonorViewSet, basename='donor')
router.register(r'requests', BloodRequestViewSet, basename='request')
router.register(r'camps', CampViewSet, basename='camp')
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('stats/', StatsView.as_view(), name='stats'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/me/', MeView.as_view(), name='auth_me'),
    path('alerts/broadcast/', BroadcastView.as_view(), name='alerts_broadcast'),
    path('', include(router.urls)),
]

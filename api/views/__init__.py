from .blood_bank import BloodBankViewSet
from .donor import DonorViewSet
from .blood_request import BloodRequestViewSet
from .camp import CampViewSet
from .campaign import CampaignViewSet
from .stats import StatsView

__all__ = [
    'BloodBankViewSet',
    'DonorViewSet',
    'BloodRequestViewSet',
    'CampViewSet',
    'CampaignViewSet',
    'StatsView'
]

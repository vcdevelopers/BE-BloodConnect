from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import BloodBank, Donor, BloodRequest, Camp, Campaign

class StatsView(APIView):
    def get(self, request, *args, **kwargs):
        total_donors = Donor.objects.count()
        active_requests = BloodRequest.objects.filter(status__in=['pending', 'approved', 'matched']).count()
        
        units_available = 0
        blood_banks = BloodBank.objects.all()
        for bb in blood_banks:
            units_available += (
                (bb.prbc_a_pos or 0) + (bb.wb_a_pos or 0) +
                (bb.prbc_a_neg or 0) + (bb.wb_a_neg or 0) +
                (bb.prbc_b_pos or 0) + (bb.wb_b_pos or 0) +
                (bb.prbc_b_neg or 0) + (bb.wb_b_neg or 0) +
                (bb.prbc_ab_pos or 0) + (bb.wb_ab_pos or 0) +
                (bb.prbc_ab_neg or 0) + (bb.wb_ab_neg or 0) +
                (bb.prbc_o_pos or 0) + (bb.wb_o_pos or 0) +
                (bb.prbc_o_neg or 0) + (bb.wb_o_neg or 0)
            )
            
        active_campaigns = Camp.objects.filter(status='upcoming').count()
        today = timezone.localdate()
        requests_today = BloodRequest.objects.filter(date=today).count()
        
        data = {
            "totalDonors": total_donors,
            "activeRequests": active_requests,
            "unitsAvailable": units_available,
            "activeCampaigns": active_campaigns,
            "requestsToday": requests_today
        }
        
        return Response(data, status=status.HTTP_200_OK)

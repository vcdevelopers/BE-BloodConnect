from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import BloodRequest, Donor
from api.serializers import BloodRequestSerializer

class BloodRequestViewSet(viewsets.ModelViewSet):
    queryset = BloodRequest.objects.all().order_by('-id')
    serializer_class = BloodRequestSerializer

    def get_queryset(self):
        queryset = self.queryset.all()
        status_param = self.request.query_params.get('status', None)
        urgency = self.request.query_params.get('urgency', None)
        
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)
        if urgency:
            queryset = queryset.filter(urgency__iexact=urgency)
        return queryset

    def perform_create(self, serializer):
        blood_group = serializer.validated_data.get('blood_group')
        matching_donors = Donor.objects.filter(blood_group=blood_group, eligible=True, status='active')
        serializer.save(matched_donors_count=matching_donors.count())

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_request(self, request, pk=None):
        blood_request = self.get_object()
        blood_request.status = 'approved'
        
        matching_donors = Donor.objects.filter(blood_group=blood_request.blood_group, eligible=True, status='active')
        blood_request.matched_donors_count = matching_donors.count()
        blood_request.save()
        
        return Response({
            "status": "success", 
            "message": f"Approved. Matched with {blood_request.matched_donors_count} donors.",
            "matched_donors": blood_request.matched_donors_count
        }, status=status.HTTP_200_OK)

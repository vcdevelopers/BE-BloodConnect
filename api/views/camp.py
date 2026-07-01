from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Camp
from api.serializers import CampSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class CampViewSet(viewsets.ModelViewSet):
    queryset = Camp.objects.all().order_by('date')
    serializer_class = CampSerializer

    def get_queryset(self):
        queryset = self.queryset.all()
        zone = self.request.query_params.get('zone', None)
        camp_status = self.request.query_params.get('status', None)
        
        if zone:
            queryset = queryset.filter(zone__iexact=zone)
        if camp_status:
            queryset = queryset.filter(status__iexact=camp_status)
        return queryset

    @action(detail=True, methods=['post'])
    def book_slot(self, request, pk=None):
        camp = self.get_object()
        if camp.slots_booked < camp.slots:
            camp.slots_booked += 1
            camp.save()
            return Response(CampSerializer(camp).data)
        return Response({'error': 'No slots available for this camp'}, status=status.HTTP_400_BAD_REQUEST)

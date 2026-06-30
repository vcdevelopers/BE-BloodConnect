import threading
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import BloodBank
from api.serializers import BloodBankSerializer
from api.scraper import run_live_scraper
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class BloodBankViewSet(viewsets.ModelViewSet):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer

    def list(self, request, *args, **kwargs):
        latest_bb = BloodBank.objects.order_by('-last_updated').first()
        needs_refresh = False
        
        if not latest_bb:
            needs_refresh = True
        else:
            time_threshold = timezone.now() - timedelta(minutes=30)
            if latest_bb.last_updated < time_threshold:
                needs_refresh = True

        if needs_refresh:
            print("[API] Local data stale. Refreshing in background...")
            threading.Thread(target=run_live_scraper).start()

        queryset = self.get_queryset()
        zone = request.query_params.get('zone', None)
        if zone:
            queryset = queryset.filter(zone__iexact=zone)

        blood_group = request.query_params.get('blood_group', None)
        if blood_group:
            col_mapping = {
                "A+": ("prbc_a_pos", "wb_a_pos"),
                "A-": ("prbc_a_neg", "wb_a_neg"),
                "B+": ("prbc_b_pos", "wb_b_pos"),
                "B-": ("prbc_b_neg", "wb_b_neg"),
                "AB+": ("prbc_ab_pos", "wb_ab_pos"),
                "AB-": ("prbc_ab_neg", "wb_ab_neg"),
                "O+": ("prbc_o_pos", "wb_o_pos"),
                "O-": ("prbc_o_neg", "wb_o_neg"),
            }
            if blood_group in col_mapping:
                prbc_col, wb_col = col_mapping[blood_group]
                queryset = queryset.filter(**{f"{prbc_col}__gt": 0}) | queryset.filter(**{f"{wb_col}__gt": 0})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='refresh')
    def refresh_data(self, request):
        # Run scraper in a background thread so the HTTP request returns immediately
        # and doesn't time out or block the client.
        threading.Thread(target=run_live_scraper).start()
        return Response({
            "status": "success", 
            "message": "Sync started in the background. The stock list will refresh automatically in a few seconds."
        }, status=status.HTTP_202_ACCEPTED)

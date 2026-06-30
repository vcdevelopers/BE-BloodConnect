from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.models import Donor
from api.services.notification import send_real_email

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class BroadcastView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        blood_group = request.data.get('bloodGroup', 'All')
        zone = request.data.get('zone', 'All')
        channel = request.data.get('channel', 'email')
        message = request.data.get('message', '')

        if not message:
            return Response({"error": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter active matching donors
        donors = Donor.objects.filter(status='active')
        recipient_ids = request.data.get('recipientIds', [])

        if recipient_ids:
            donors = donors.filter(id__in=recipient_ids)
        else:
            if blood_group != 'All':
                donors = donors.filter(blood_group__iexact=blood_group)
            if zone != 'All':
                donors = donors.filter(zone__iexact=zone)

        recipient_emails = [d.email for d in donors if d.email]

        template_id = request.data.get('templateId', '')

        if channel == 'email':
            if recipient_emails:
                subject = "Emergency Alert - Mumbai Blood Connect"
                success = send_real_email(subject, message, recipient_emails)
                if success:
                    return Response({
                        "status": "success",
                        "recipients": len(recipient_emails),
                        "message": f"Broadcast email successfully sent to {len(recipient_emails)} donors."
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "error",
                        "message": "Failed to send email via SMTP server configuration."
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({
                    "status": "success",
                    "recipients": 0,
                    "message": "No matching donors found with registered email addresses."
                }, status=status.HTTP_200_OK)
        elif channel == 'sms':
            if not template_id:
                return Response({"error": "DLT Template ID is required for sending SMS alerts."}, status=status.HTTP_400_BAD_REQUEST)
                
            from api.services.notification import send_dlt_sms_routemobile
            recipient_phones = [d.phone for d in donors if d.phone]
            sent_count = 0
            last_message = ""
            
            for phone in recipient_phones:
                success, status_msg = send_dlt_sms_routemobile(phone, message, template_id)
                last_message = status_msg
                if success:
                    sent_count += 1
                    
            if sent_count > 0:
                return Response({
                    "status": "success",
                    "recipients": sent_count,
                    "message": f"Broadcast SMS successfully dispatched to {sent_count} donors via Route Mobile."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": f"Failed to dispatch SMS. Gateway response: {last_message}"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Simulate other channels
            return Response({
                "status": "success",
                "recipients": donors.count(),
                "message": f"[Simulation] Broadcast sent to {donors.count()} donors via {channel.upper()}."
            }, status=status.HTTP_200_OK)
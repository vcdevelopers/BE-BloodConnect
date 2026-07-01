from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import BloodRequest, Donor
from api.serializers import BloodRequestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
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
        
        # Save the request database record
        blood_request = serializer.save(matched_donors_count=matching_donors.count())

        # Send alert email notification to admin/client
        try:
            from django.conf import settings
            from api.services.notification import send_real_email
            
            admin_emails = [
                e.strip() for e in getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', 'noreply@vibecopilot.ai').split(',') if e.strip()
            ]
            
            if admin_emails:
                subject = f"🚨 New Blood Request: {blood_request.blood_group} Required"
                message = (
                    f"Hello Admin,\n\n"
                    f"A new blood request has been submitted on Mumbai Blood Connect:\n\n"
                    f"Details:\n"
                    f"- Patient Name: {blood_request.patient_name}\n"
                    f"- Required Blood Group: {blood_request.blood_group}\n"
                    f"- Units Needed: {blood_request.units}\n"
                    f"- Hospital Name: {blood_request.hospital}\n"
                    f"- Hospital Location: {blood_request.hospital_address}\n"
                    f"- Urgency Level: {blood_request.urgency.upper()}\n"
                    f"- Attendant Name: {blood_request.attendant_name}\n"
                    f"- Mobile Number: {blood_request.phone}\n\n"
                    f"Please log in to the Admin Dashboard to review and approve this request.\n\n"
                    f"Best regards,\n"
                    f"Mumbai Blood Connect System"
                )
                send_real_email(subject, message, admin_emails)
        except Exception as err:
            print(f"[Error] Failed to send admin email notification: {err}")

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_request(self, request, pk=None):
        blood_request = self.get_object()
        blood_request.status = 'approved'
        
        matching_donors = Donor.objects.filter(blood_group=blood_request.blood_group, eligible=True, status='active')
        blood_request.matched_donors_count = matching_donors.count()
        blood_request.save()
        
        # Dispatch emails to all matching active eligible donors
        from api.services.notification import send_real_email
        recipient_emails = [d.email for d in matching_donors if d.email]
        
        if recipient_emails:
            subject = f"EMERGENCY: {blood_request.blood_group} Blood Required"
            message = (
                f"Emergency Blood Request Alert!\n\n"
                f"An urgent request for {blood_request.blood_group} blood has been approved near you.\n\n"
                f"Request Details:\n"
                f"- Patient: {blood_request.patient_name}\n"
                f"- Required Units: {blood_request.units}\n"
                f"- Hospital: {blood_request.hospital}\n"
                f"- Location Address: {blood_request.hospital_address}\n"
                f"- Urgency Level: {blood_request.urgency.upper()}\n"
                f"- Attendant/Contact Person: {blood_request.attendant_name} (Phone: {blood_request.phone})\n\n"
                f"If you are eligible and can donate, please contact the attendant directly to save a life.\n\n"
                f"Best regards,\n"
                f"Mumbai Blood Connect Team"
            )
            # Send alert email
            send_real_email(subject, message, recipient_emails)
        
        return Response({
            "status": "success", 
            "message": f"Approved. Matched and alerted {len(recipient_emails)} donors via email.",
            "matched_donors": blood_request.matched_donors_count
        }, status=status.HTTP_200_OK)

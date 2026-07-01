from rest_framework import viewsets
from api.models import Donor
from api.serializers import DonorSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all().order_by('-id')
    serializer_class = DonorSerializer

    def get_queryset(self):
        queryset = self.queryset.all()
        zone = self.request.query_params.get('zone', None)
        blood_group = self.request.query_params.get('blood_group', None)
        
        if zone:
            queryset = queryset.filter(zone__iexact=zone)
        if blood_group:
            queryset = queryset.filter(blood_group__iexact=blood_group)
        return queryset

    def perform_create(self, serializer):
        donor = serializer.save()
        if donor.email:
            subject = "Welcome to Mumbai Blood Connect - Donor Registration Successful"
            message = (
                f"Dear {donor.name},\n\n"
                f"Thank you for registering as a blood donor on Mumbai Blood Connect. "
                f"Your account is registered under the '{donor.blood_group}' blood group in the '{donor.zone}' area.\n\n"
                f"In case of an emergency requirement for your blood group, you will receive an alert from us.\n\n"
                f"Thank you for helping us save lives.\n\n"
                f"Best regards,\n"
                f"Mumbai Blood Connect Team"
            )
            from api.services.notification import send_real_email
            send_real_email(subject, message, [donor.email])

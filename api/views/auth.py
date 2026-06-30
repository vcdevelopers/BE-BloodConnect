from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Find username mapped to this email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = email # Fallback

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                "status": "success",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff
                }
            }, status=status.HTTP_200_OK)
            
        return Response({
            "status": "error",
            "message": "Invalid email or password."
        }, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    authentication_classes = []

    def post(self, request):
        logout(request)
        return Response({"status": "success", "message": "Logged out successfully."}, status=status.HTTP_200_OK)


from rest_framework.authentication import SessionAuthentication

class MeView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "authenticated": True,
                "user": {
                    "username": request.user.username,
                    "email": request.user.email,
                    "is_staff": request.user.is_staff
                }
            })
        return Response({"authenticated": False})
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsAdmin, IsTrader

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LogoutView(generics.GenericAPIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e: # TODO: log error
            return Response({"error": "Invalid token"}, status=400)

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})

class TraderOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsTrader]

    def get(self, request):
        return Response({"message": "Hello, Trader!"})

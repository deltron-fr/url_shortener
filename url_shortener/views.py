from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import ShortURL, CustomUser
from .serializer import ShortURLSerializer, UserSerializer

class ShortURLCreateAPIView(generics.CreateAPIView):

    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

class CreateUserAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    permission_classes = [AllowAny]

class URLDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "login successful"}, status=status.HTTP_200_OK)
    
        return Response({"error": "invalid authentication credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT)


def redirect_to_original(request, short_code):
    link = get_object_or_404(ShortURL, short_code=short_code)
    return redirect(link.original_url)

class HealthView(APIView):
    def get(self):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

    


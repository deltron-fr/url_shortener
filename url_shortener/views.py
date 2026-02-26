from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404, redirect
from .models import ShortURL, CustomUser
from .serializer import ShortURLSerializer

class ShortURLCreateAPIView(generics.ListCreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

def redirect_to_original(request, short_code):
    link = get_object_or_404(ShortURL, short_code=short_code)
    return redirect(link.original_url)

class HealthView(generics.GenericAPIView):
    def get(self, request):
        return Response({"status": "ok"})

def RegisterView(request):
    CustomUser.objects.create_user(
        username=request.POST['username'],
        email=request.POST['email'],
        password=request.POST['password']
    )
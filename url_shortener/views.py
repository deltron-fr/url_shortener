from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from .models import ShortURL, CustomUser, PasswordResetToken
from .serializer import ShortURLSerializer, UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .rate_limiter import UserTypeRateThrottle
import secrets
import hashlib

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

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "login successful", "token": token.key}, status=status.HTTP_200_OK)
    
        return Response({"error": "invalid authentication credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
       
        try:
            user = CustomUser.objects.get(email=email)

            PasswordResetToken.objects.filter(
                user=user,
                is_used=False
            ).delete()


            token = secrets.token_urlsafe(32)
            hashed_token = hashlib.sha256(token.encode()).hexdigest()

            PasswordResetToken.objects.create(
                user=user,
                token=hashed_token
            )

            send_mail(
                subject="Password Reset",
                message=f"Your reset token: {token}",
                from_email=None,
                recipient_list=[email],
            )

        except CustomUser.DoesNotExist:
            pass

        return Response({"If this is a registered email, a reset token has been sent"}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        user = serializer.validated_data["user"]
        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        reset_token.is_used = True
        reset_token.save()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)


class RedirectAPIView(APIView):
    throttle_classes = [UserTypeRateThrottle]
    def get(self, request, short_code):

        link = get_object_or_404(ShortURL, short_code=short_code)
        return redirect(link.original_url)

class HealthView(APIView):
    def get(self):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

    


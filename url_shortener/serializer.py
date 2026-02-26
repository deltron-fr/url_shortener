from rest_framework import serializers
from .models import ShortURL, CustomUser, PasswordResetToken
import hashlib

class ShortURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_code', 'short_url', 'created_at']
        read_only_fields = ['short_code', 'created_at']

    def get_short_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f"/{obj.short_code}/")
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'plan']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=64)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        token = attrs.get("token")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        try:
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            reset_token = PasswordResetToken.objects.get(
                user=user,
                token=hashed_token,
                is_used=False
            )
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not reset_token.is_valid():
            raise serializers.ValidationError("Token expired")

        attrs["user"] = user
        attrs["reset_token"] = reset_token
        return attrs


     

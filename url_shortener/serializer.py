from rest_framework import serializers
from .models import ShortURL, CustomUser

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

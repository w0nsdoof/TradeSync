from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "profile_picture"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role", "profile_picture"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

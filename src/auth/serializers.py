from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer for Return id, usernam 
    to use it inside other serializer.
    """
    class Meta:
        model = User
        fields = ("id", "username")


class SignupSerializer(serializers.ModelSerializer):
    """
    Signup user with username, password and 
    Return id, username.
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ["id", "username", "password"]

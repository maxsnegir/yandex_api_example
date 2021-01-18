from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class JWTSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.UUIDField()

    def validate(self, data):
        user = get_object_or_404(User, email=data['email'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError("Неверный код")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'email',
                  'role']

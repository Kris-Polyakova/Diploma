from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .validators import validate_username

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password', 'password2']

    def validate_username(self, value):
        validate_username(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        try:
            validate_password(attrs['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        password = attrs['password']
        if not any(c.isupper() for c in password):
            raise serializers.ValidationError({"password": "Пароль должен содержать хотя бы одну заглавную букву."})
        if not any(c.isdigit() for c in password):
            raise serializers.ValidationError({"password": "Пароль должен содержать хотя бы одну цифру."})
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>/?`~" for c in password):
            raise serializers.ValidationError({"password": "Пароль должен содержать хотя бы один специальный символ."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', '')
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'is_admin']


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'is_admin', 'is_active']

    def validate_username(self, value):
        from .validators import validate_username
        validate_username(value)
        return value
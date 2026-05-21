from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .validators import validate_username, validate_password_strength

User = get_user_model()

class AdminUserListSerializer(serializers.ModelSerializer):
    files_count = serializers.IntegerField(read_only=True)
    total_size = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'email',
            'is_admin',
            'date_joined',
            'files_count',
            'total_size'
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password', 'password2']

    def validate_username(self, value):
        from .validators import validate_username
        validate_username(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        password = attrs['password']

        validate_password(password)
        validate_password_strength(password)

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
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
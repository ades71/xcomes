import datetime
import jwt
from django.conf import settings

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'nickname',
            'name',
            'phone_number',
            'is_terms_agreement',
            'is_info_use_agreement',
            'token'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    expiration_date = serializers.CharField(max_length=255, read_only=True)
    membership_level = serializers.CharField(max_length=20, read_only=True)
    access_key = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        user.last_login = timezone.now()

        payload = {'id': user.id,
                   'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
                   'iat': datetime.datetime.now()
                   }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        user.access_key = token.decode('utf-8')

        user.save(update_fields=['last_login', 'access_key'])

        res_data = {
            'email': user.email,
            'membership_level': user.membership_level,
            'expiration_date': user.expiration_date,
            'access_key': user.access_key
        }
        return res_data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',
            'access_key'
        ]

        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

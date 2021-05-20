from . import models
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Логин")
    password = serializers.CharField(label="Пароль", style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = 'Аккаунт не активен.'
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = 'Невозможно войти с предоставленными данными.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Должен включать "Логин" и "Пароль".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = (
            'name',
            'bill',
            'locale'
        )
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import random
from common.redis_client import save_confirmation_code, get_confirmation_code, delete_confirmation_code

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    birthdate = serializers.DateField(required=False, allow_null=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create_user(
            email=email,
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            birthdate=validated_data.get('birthdate'),
            is_active=False
        )

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        save_confirmation_code(email, code)
        print(f"=== Redis Confirmation Code for {email}: {code} ===")
        return user

class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        entered_code = data['code']

        saved_code = get_confirmation_code(email)
        if not saved_code:
            raise ValidationError("Код подтверждения не найден или истек срок его действия.")

        if saved_code != entered_code:
            raise ValidationError("Неверный код подтверждения.")

        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        delete_confirmation_code(email)
        return user

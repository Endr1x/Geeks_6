from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import random
from .models import Category, Product, Review, UserConfirmation
from common.validators import validate_user_age

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        if not value.strip():
            raise ValidationError("Текст отзыва не может быть пустым.")
        return value

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise ValidationError("Количество звезд должно быть в диапазоне от 1 до 5.")
        return value

class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def validate(self, attrs):
        validate_user_age(self.context.get('request'))
        return attrs

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum([r.stars for r in reviews]) / reviews.count(), 1)
        return 0

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Цена товара должна быть больше нуля.")
        return value

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise ValidationError("Название товара должно содержать хотя бы 2 символа.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise ValidationError("Название категории должно содержать хотя бы 2 символа.")
        return value

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
        phone = validated_data.get('phone_number', '')
        birthdate = validated_data.get('birthdate', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=phone if phone else None,
            birthdate=birthdate,
            is_active=False
        )
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        UserConfirmation.objects.create(user=user, code=code)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return {'user': user}
        raise ValidationError("Неверные учетные данные или пользователь не активен.")

class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            confirmation = UserConfirmation.objects.get(user=user)
        except (User.DoesNotExist, UserConfirmation.DoesNotExist):
            raise ValidationError("Пользователь или код подтверждения не найден.")

        if confirmation.code != data['code']:
            raise ValidationError("Неверный код подтверждения.")
        
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.save()
        user.confirmation.delete()
        return user

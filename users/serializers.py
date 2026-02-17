from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.core.mail import send_mail
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует"})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Пользователь с таким именем уже существует"})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        code = user.generate_confirmation_code()
        print(f"Код подтверждения для {user.email}: {code}")
        
        # Для продакшена:
        # send_mail(
        #     'Подтверждение регистрации',
        #     f'Ваш код подтверждения: {code}',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email],
        #     fail_silently=False,
        # )
        
        return user

class ConfirmUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'], confirmation_code=data['code'])
            if user.is_active:
                raise serializers.ValidationError("Пользователь уже подтвержден")
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный email или код подтверждения")
        
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        
        if user and user.is_active:
            return user
        elif user and not user.is_active:
            raise serializers.ValidationError("Пожалуйста, подтвердите свой email")
        else:
            raise serializers.ValidationError("Неверное имя пользователя или пароль")
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import RegisterSerializer, ConfirmUserSerializer, LoginSerializer
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Пользователь создан. Проверьте email для подтверждения.',
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_user(request):
    serializer = ConfirmUserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Активируем пользователя
        user.is_active = True
        user.confirmation_code = None  # Очищаем код
        user.save()
        
        # Создаем токен для автоматического входа
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Пользователь успешно подтвержден',
            'token': token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)
        
        # Создаем или получаем токен
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Успешный вход',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Успешный выход'}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Ошибка при выходе'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profile(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active
    })
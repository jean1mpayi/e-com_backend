from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_avatar(request):
    user = request.user
    if 'avatar' not in request.FILES:
        return Response({'detail': 'Aucun fichier fourni'}, status=status.HTTP_400_BAD_REQUEST)
    
    profile = user.profile
    profile.avatar = request.FILES['avatar']
    profile.save()
    
    return Response({'avatar': profile.avatar.url}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    try:
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'detail': 'Un utilisateur avec cet email existe déjà'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = User.objects.create(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
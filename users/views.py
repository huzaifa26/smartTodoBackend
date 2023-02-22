from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer
from .serializers import LoginSerializer

class signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # token = Token.objects.create(user=user)
            return Response({'token': "token.key"})
        return Response(serializer.errors, status=400)
    

class login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # token, created = Token.objects.get_or_create(user=user)
            return Response({'token': "token.key"})
        return Response(serializer.errors, status=400)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from .serializers import UserSerializer
from .serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404



class signup(generics.CreateAPIView):
    User = get_user_model()

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': "token.key"})
        return Response(serializer.errors, status=400)
    

class login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user,data = serializer.validated_data
            user=user['user']
            token,created = Token.objects.get_or_create(user=user)
            # data.token=token.key
            return Response({'token': token.key,"data":data})
        return Response(serializer.errors, status=400)
    
# class UpdateUserView(generics.CreateAPIView):
#     def put(self, request):
#         try:
#             User=get_user_model()
#             user = User.objects.get(id=request.data['id'])
#             user.username = request.data['username']
#             user.email = request.data['email']
#             user.first_name = request.data['first_name']
#             user.last_name = request.data['last_name']

#             user.save()

#             return Response({'message': 'User details updated successfully',"data":user})

#         except User.DoesNotExist:
#             # If the user instance does not exist, return an error response
#             return Response({'error': 'User does not exist'})

#         except Exception as e:
#             # If any other error occurs, return a server error response
#             return Response({'error': str(e)})

class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(id=request.data['id'])
            serializer = self.serializer_class(user, data=request.data, partial=True)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data,)
            return Response(serializer.errors)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'})
        except Exception as e:
            return Response({'error': str(e)})

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from datetime import datetime
from django.contrib.auth.models import User


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data['user'])
        request.data['user'] = user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.data["user"])


class UserTodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = request.data['user']
        user = get_object_or_404(User, id=user_id)
        today = request.data['date']
        queryset = Todo.objects.filter(user=user, added_date__date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    # def get_queryset(self):
    #     user_id = self.kwargs['user_id']
    #     user = get_object_or_404(User, id=user_id)
    #     today = datetime.now().date()
    #     queryset = Todo.objects.filter(user=user, added_date__date=today)
    #     return queryset


class TodoListUpdateView(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    
    def update(self, request, *args, **kwargs):
        print(request.data)
        user = get_object_or_404(User, id=request.data['user'])
        request.data['user'] = user
        todo = get_object_or_404(Todo, id=request.data['id'], user=user)
        print(user)
        print(todo)
        serializer = self.get_serializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

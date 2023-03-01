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
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        print(self.request.data["user"])
        serializer.save(user=self.request.data["user"])

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        today = datetime.now().date()
        queryset = Todo.objects.filter(user=user, added_date__date=today)
        return queryset

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
    #     self.check_object_permissions(self.request, obj)
    #     return obj


class UserTodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        today = datetime.now().date()
        queryset = Todo.objects.filter(user=user, added_date__date=today)
        return queryset

from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics
from django.db.models import Count
from datetime import date, timedelta
from django.db.models import Count, Case, When, IntegerField



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
        serializer.save(
            user=self.request.data["user"], added_date=self.request.data["added_date"])


class UserTodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = request.data['user']
        user = get_object_or_404(User, id=user_id)
        today = request.data['date']
        queryset = Todo.objects.filter(user=user, start_time__date=today).order_by('start_time')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class TodoListUpdateView(generics.UpdateAPIView):
    serializer_class = TodoSerializer

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data['user'])
        request.data['user'] = user
        todo = get_object_or_404(Todo, id=request.data['id'], user=user)
        serializer = self.get_serializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TaskCountView(generics.GenericAPIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user'))
        target_date = kwargs.get('date')
        target_date = target_date[0:11]

        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=30)

        queryset = Todo.objects.filter(user=user,start_time__range=(start_date, end_date))
        queryset = queryset.annotate(day=TruncDate('start_time'))
        queryset = queryset.values('day').annotate(total=Count('id'),completed=Count(Case(When(completed=True, then=1), output_field=IntegerField()))).order_by('-day')

        for todo in queryset:
            print(todo)

        task_count = Todo.objects.filter(user=user, start_time__date=target_date).count()
        completed_count = Todo.objects.filter(user=user, start_time__date=target_date, completed=True).count()
        started_count = Todo.objects.filter(user=user, start_time__date=target_date, completed=False, started=True).count()

        return Response({'task_count': task_count, 'completed_count': completed_count, "started_count": started_count, "month_count": queryset})


class TodoTimeline(generics.GenericAPIView):
    def get(self, request,*args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user'))
        today = date.today()
        end_date = today + timedelta(days=6)
        todos = Todo.objects.filter(user=user,start_time__date__gte=today, start_time__date__lte=end_date).order_by('start_time')
        timeline = [[[] for _ in range(7)] for _ in range(10)] 
        labels = []

        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i in range(7):
            date_for_label = today + timedelta(days=i)
            day_name = day_names[date_for_label.weekday()]
            
            labels.append(date_for_label)

        for todo in todos:
            index = (todo.start_time.date() - today).days
            task_index = 0 
            while task_index < 10:
                if not timeline[task_index][index]:
                    timeline[task_index][index] = [todo.start_time.hour + todo.start_time.minute/100, todo.end_time.hour + todo.end_time.minute/100]
                    break
                task_index += 1

        data = []
        colors = ['#AF91E9', '#0E123F']

        for i in range(10): 
            color_index = i % 2
            diction = {
                "label": f"Task {i+1}",
                "data": timeline[i],
                "borderColor": colors[color_index],
                "backgroundColor": colors[color_index],
            }
            data.append(diction)

        return Response({"timeline": data, "labels": labels})
    

class TodoListDeleteView(generics.GenericAPIView):
    serializer_class = TodoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user'))
        todo = get_object_or_404(Todo, user_id=user, id=kwargs.get("id"))
        print(user,kwargs.get("id"))
        todo.delete()
        return Response(status=204)
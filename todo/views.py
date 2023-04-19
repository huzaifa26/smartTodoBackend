from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model

from rest_framework import generics
from django.db.models import Count
from datetime import date, timedelta
from django.db.models import Count, Case, When, IntegerField
from django.db.models import Sum
from django.utils import timezone

import requests
from bs4 import BeautifulSoup
import json
import re


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = get_object_or_404(get_user_model(), id=data['user'])
        data['user'] = user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.data["user"], added_date=self.request.data["added_date"])


class UserTodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data['user']
        user = get_object_or_404(get_user_model(), id=user_id)
        today = request.data['date']
        queryset = Todo.objects.filter(
            user=user, added_date__date=today).order_by('added_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class TodoListUpdateView(generics.UpdateAPIView):
    serializer_class = TodoSerializer

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=request.data['user'])
        request.data['user'] = user
        todo = get_object_or_404(Todo, id=request.data['id'], user=user)
        serializer = self.get_serializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TaskCountView(generics.GenericAPIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=kwargs.get('user'))
        target_date = kwargs.get('date')
        target_date = target_date[0:11]

        todayDate=timezone.now().date()
        end_date = todayDate-timezone.timedelta(days=1)
        start_date = todayDate - timezone.timedelta(days=7)

        queryset = Todo.objects.filter(user=user, added_date__range=(start_date, end_date))
        queryset = queryset.annotate(day=TruncDate('added_date'))
        queryset = queryset.values('day').annotate(total=Count('id'), completed=Count(Case(When(completed=True, then=1), output_field=IntegerField()))).order_by('-day')

        date_list = [start_date + timezone.timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        lastSeven = []
        for date in date_list:
            task_count = {'date': date}
            tasks = queryset.filter(day=date)
            if tasks:
                task_count['total'] = tasks[0]['total']
                task_count['completed'] = tasks[0]['completed']
            else:
                task_count['total'] = 0
                task_count['completed'] = 0
            lastSeven.append(task_count)

        task_count = Todo.objects.filter(user=user, added_date__date=target_date, started=False).count()
        completed_count = Todo.objects.filter(user=user, added_date__date=target_date, completed=True).count()
        started_count = Todo.objects.filter(user=user, added_date__date=target_date, completed=False, started=True).count()

        return Response({'task_count': task_count, 'completed_count': completed_count, "started_count": started_count, "month_count": lastSeven})


class TodoTimeline(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=kwargs.get('user'))
        today = date.today()
        end_date = today + timedelta(days=6)
        todos = Todo.objects.filter(
            user=user, start_time__date__gte=today, start_time__date__lte=end_date, start_time__isnull=False, end_time__isnull=False).order_by('start_time')
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
                    timeline[task_index][index] = [todo.start_time.hour +
                                                   todo.start_time.minute/100, todo.end_time.hour + todo.end_time.minute/100]
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
        user = get_object_or_404(get_user_model(), id=kwargs.get('user'))
        todo = get_object_or_404(Todo, user_id=user, id=kwargs.get("id"))
        print(user, kwargs.get("id"))
        todo.delete()
        return Response(status=204)


class TodayTotalTimeView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        time = kwargs.get("time")
        time = datetime.strptime(time, '%a %b %d %Y %H:%M:%S GMT%z (%Z)')
        time = time.date()
        # Get the current date and time in the server's timezone
        # today = timezone.now().date()
        # Filter the Todo objects that have a start_time set to today's date
        todos = Todo.objects.filter(added_date__date=time)

        # Calculate the total time for the filtered todos
        total_time = todos.aggregate(Sum('totalTime'))['totalTime__sum'] or 0

        # Return the total time as a JSON response
        print(todos)
        return Response({'today_total_time': total_time})


class Get_weather_data(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        location = kwargs.get("location")
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Language": "en-US,en;q=0.5",
        }
        url = 'https://www.google.com/search?q=weather+'+location
        session = requests.Session()
        session.headers["User-Agent"] = header["User-Agent"]
        session.headers["Accept-Language"] = header["Language"]
        session.headers["Content-Language"] = header["Language"]

        html = session.get(url)
        base = BeautifulSoup(html.text, "html.parser")
        data_in = re.search(r"pmc='({.*?})'", html.text).group(1)
        data_in = json.loads(data_in.replace(
            r"\x22", '"').replace(r'\\"', r"\""))
        data_out = list()
        output_units = {"temp": "F", "speed": "mph"}

        for entry_in in data_in["wobnm"]["wobhl"][:5]:
            entry_out = {
                "datetime": entry_in["dts"],
                "weather": entry_in["c"],
                "icon": entry_in["iu"],
                "humidity": float(entry_in["h"].replace("%", "")),
                "precip_prob": float(entry_in["p"].replace("%", ""))
            }
            temp_key = "tm"
            entry_out["temp"] = int((float(entry_in[temp_key]) * 1.8) + 32)
            entry_out["unit"] = output_units["temp"]
            speed_key = "ws"
            entry_out["wind_speed"] = float(
                entry_in[speed_key].replace("km/h", "").replace("mph", ""))
            icon_element = base.find('img', {'class': 'wob_tci'})
            if icon_element is not None:
                icon_url = icon_element['src']
            entry_out["icon_url"] = icon_url
            data_out.append(entry_out)

        return Response({"weather": data_out})

from django.urls import path
from .views import TodoListCreateView
from .views import UserTodoListView
from .views import TodoListUpdateView
from .views import TaskCountView
from .views import TodoTimeline

urlpatterns = [
    path('add/', TodoListCreateView.as_view(), name='add-todo-list'),
    path('get/', UserTodoListView.as_view(), name='user_todo_list_today'),
    path('edit/', TodoListUpdateView.as_view(), name='user_todo_list_edit'),
    path('count/<int:user>/<str:date>/', TaskCountView.as_view(), name='task_count'),
    path('timeline/<int:user>', TodoTimeline.as_view(), name='time_line_data'),

]
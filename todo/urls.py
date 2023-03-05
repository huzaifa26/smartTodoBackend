from django.urls import path
from .views import TodoListCreateView
from .views import UserTodoListView
from .views import TodoListUpdateView

urlpatterns = [
    path('add/', TodoListCreateView.as_view(), name='add-todo-list'),
    path('get/', UserTodoListView.as_view(), name='user_todo_list_today'),
    path('edit/', TodoListUpdateView.as_view(), name='user_todo_list_edit'),

]
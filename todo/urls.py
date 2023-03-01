from django.urls import path
from .views import TodoListCreateView
from .views import UserTodoListView

urlpatterns = [
    path('add/', TodoListCreateView.as_view(), name='add-todo-list'),
    path('today/<int:user_id>', UserTodoListView.as_view(), name='user_todo_list_today'),

]
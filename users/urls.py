from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup.as_view(), name='signup'),
    path('login/', views.login.as_view(), name='login'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]

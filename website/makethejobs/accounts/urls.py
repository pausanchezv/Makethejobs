from django.contrib.auth import login
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login.as_view(), name='login'),
]
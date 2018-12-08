
from django.urls import path

from . import views

urlpatterns = [
    path('userhome/', views.UserHome.as_view(), name='userhome'),
]
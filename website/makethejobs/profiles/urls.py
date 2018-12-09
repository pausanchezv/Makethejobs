
from django.urls import path

from . import views

urlpatterns = [
    path('private/me/', views.UserHome.as_view(), name='userhome'),
]
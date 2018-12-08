
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('userhome/', views.home, name='userhome'),
]
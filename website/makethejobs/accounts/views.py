from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Accounts. You're at the makethejobs index.")
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.apps import apps
from .models import *

def home(request):

    return render(request, "collection/index.html")

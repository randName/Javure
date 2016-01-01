from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")

@login_required
def home(request):
    return render(request, 'index.html')

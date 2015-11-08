from django.shortcuts import render

def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")

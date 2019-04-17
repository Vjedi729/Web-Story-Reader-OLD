from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'navigator/home.html')

def about(request):
    return HttpResponse('<h1>Project Web Story Reader - About Us</h1>')

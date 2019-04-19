from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    return render(request, 'navigator/home.html')

def about(request):
    return HttpResponse('<h1>Project Web Story Reader - About Us</h1>')

def register(request):
    form = UserCreationForm()
    return renter(request, 'navigator/register.html', {'form':form})

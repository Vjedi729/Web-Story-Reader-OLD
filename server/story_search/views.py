from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def search_filter(request):
    return HttpResponse('<h1>Search Page</h1>')
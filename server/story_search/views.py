from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def search_filter(request):
    return HttpResponse('<h1>Search Page</h1>')

#from fanfic_scraper import ao3_scraper

def api(request):
    query_json = request.body
    json = "Some Json Probably"
    return HttpResponse(json, content_type='application/json')

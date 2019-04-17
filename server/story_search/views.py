from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def search_filter(request):
    return HttpResponse('<h1>Search Page</h1>')

import fanfic_scraper as ffs

def api(request):
    query_json = request.body
    json = "Some Json Probably"
    return HttpResponse(json, content_type='application/json')

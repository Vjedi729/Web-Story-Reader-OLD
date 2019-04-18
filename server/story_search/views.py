from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def search_filter(request):
    return HttpResponse('<h1>Search Page</h1>')

from .website_crawler import Ao3_crawler
def update_ao3(request):
    Ao3_crawler(limit = 1000)
    return HttpResponse('<h1>Update Complete, Check Admin Page</h1>')

def api(request):
    query_json = request.body
    json = "Some Json Probably"
    return HttpResponse(json, content_type='application/json')

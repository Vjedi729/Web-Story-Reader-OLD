from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def search_filter(request):
    return HttpResponse('<h1>Search Page Does Not Exist Yet</h1>')

from .website_crawler import Ao3_Crawler
def update_ao3(request):
    json = Ao3_Crawler(limit = 45, skip = 0).toJson()
    return HttpResponse(json, content_type='application/json')

from story_search.wsr_story import WSR_Story_Query, WSR_Story, StoryType
def search_api(request):
    query_json = request.body
    if len(query_json) > 0:
        query_dict = json.loads(query_json)
    else:
        query_dict = {}
    query = WSR_Story_Query(query_dict)
    results = query.get_stories()

    myjson = '{ "results":[\n'
    for story in results.all():
        wsr_story = WSR_Story(StoryType.DB, story)
        myjson += "\n" + wsr_story.toJson() + ","
    myjson = myjson[:-1] + '\n] }'
    return HttpResponse(myjson, content_type='application/json')

def read_list_api(request):
    if request.method == 'GET':
        return HttpResponse('')
    elif request.method == 'POST':
        r_json = request.body
        r_dict = json.loads(r_json)
        r_type = r_dict.get('type')
        r_story_id = r_dict.get('story_id')
        return HttpResponse('')

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
        myjson += "\n" + wsr_story.toJson(indent=2) + ","
    myjson = myjson[:-1] + '\n] }'
    return HttpResponse(myjson, content_type='application/json')

# FIXME: Missing User Checking
import story_search.json_utils as j
def read_list_api(request):
    if request.method == 'GET':
        recs = Read_Record.objects.all()

        to_read = recs.filter(type="TO_READ")
        read = recs.filter(type="MARK_READ")
        tr_json = j.list_to_json_list([WSR_Story(StoryType.DB, rec.chapter.story) for rec in to_read])

        resp_json = '{ "to_read":'+tr_json+'}'
        return HttpResponse(resp_json, content_type='application/json')
    elif request.method == 'POST':
        r_json = request.body
        r_dict = json.loads(r_json)
        r_type = str(r_dict.get('type'))
        r_story_id = int(r_dict.get('story_id'))
        r_chapter_num = int(r_dict.get('chap_num', default=1))
        #try:
        chap = Chapter.objects.get(story = r_story_id, number = r_chapter_num)
        #except Chapter.DoesNotExist:
        #   pass
        try:
            read_rec = Read_Record.objects.get(chapter=chap, type = r_type)
            read_rec.delete()
        except Read_Record.DoesNotExist:
            read_rec = Read_Record(chapter=chap)
            read_rec.save()
        return HttpResponse('')

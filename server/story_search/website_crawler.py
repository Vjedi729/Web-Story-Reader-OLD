# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:46:05 2019

@author: Vishal Patel
"""
import urllib
from bs4 import BeautifulSoup
import json

import time

from .scrapers import Ao3_Story, FFnet_Story
from .wsr_story import WSR_Story, StoryType
from story_search.models import Ao3_Fandom, Ao3_Story_Tracker

# Internal
#import parse_utils as p

class Ao3_crawler:
    base_site = "https://archiveofourown.org"
    test_fandom_list = "https://archiveofourown.org/media/Anime%20*a*%20Manga/fandoms"
    test_fandom = "https://archiveofourown.org/tags/1984%20-%20George%20Orwell/works"
    def __init__(self, delay = 0.75, limit=None):
        self.debug = True

        for name, url in Ao3_crawler.parse_one_fandom_list(Ao3_crawler.test_fandom_list):
            Ao3_Fandom(name=name, url=url).save()

        pages_read = 0
        for fandom in Ao3_Fandom.objects:
            if limit is not None and limit - pages_read < 0:
                return
            if(self.debug):
                print("("+str(pages_read)+") Reading", fandom.name, "Fandom Page:", end = " ")
            stories, result_pages = Ao3_crawler.parse_one_fandom(fandom.url, delay=delay)
            if(self.debug):
                print("\thas", len(stories), "stories and", result_pages, "page(s) of results.")
            pages_read += result_pages
            # for name, url in stories:
            #     Ao3_Story_Tracker(url = url)
            #     load_time = time.time()
            #     story = WSR_Story(StoryType.Ao3, Ao3_Story(story_url))
            #     time.sleep(delay - (time.time()-load_time))

    def parse_one_fandom_list(fandom_list_url):
        fandoms = []

        page = urllib.request.urlopen(fandom_list_url)
        html = BeautifulSoup(page, 'html.parser')
        inner_main = html.find('div', {'id':'main'})

        fandom_index = inner_main.find('ol', {'class':'alphabet fandom index group'})
        letter_boxes = fandom_index.find_all('li',{"class":'letter listbox group'})
        if(self.debug):
            print('Reading Boxes:', end=" ")
        for lb in letter_boxes:
            if(self.debug):
                print(lb.get('id')[-1], end = " ")
            name_boxes = lb.find('ul', {'class':'tags index group'}).find_all('li')
            for nb in name_boxes:
                x = nb.find('a')
                fandoms.append( (x.text, Ao3_crawler.base_site+x.get('href')) )
        if(self.debug):
            print("")
            print("")

        return fandoms

    def parse_one_fandom(fandom_page_1_url, delay = 1):
        curr_page_url = fandom_page_1_url
        stories = []
        i = 0
        #print('\t\tReading Page:', end=" ")
        while True:
            i+=1
            if(self.debug):
                print(i, end = " ")#curr_page_url)

            # Load and read page
            loaded = False
            while not loaded:
                try:
                    page = urllib.request.urlopen(curr_page_url)
                    load_time = time.time()
                    loaded = True
                except:
                    if(self.debug):
                        print("Load from", curr_page_url, "failed. Retrying...")
                    loaded = False

            html = BeautifulSoup(page, 'html.parser')
            inner_main = html.find('div', {'id':'main'})

            #Collect URLs
            info_boxes = inner_main.find_all('li', {'class':'work blurb group', 'role':'article'})
            for ib in info_boxes:
                title_box = ib.find('h4', {'class':'heading'})
                title = title_box.find('a')
                stories.append( (title.text, Ao3_crawler.base_site+title.get("href")) )

            # Find next page
            temp = inner_main.find('ol', {'class':'pagination actions'})
            if temp is None:
                next_button = None
            else:
                next_button = temp.find('a', {'rel':'next'})
            # Stop at last page
            if next_button is None:
                break
            else:
                curr_page_url = Ao3_crawler.base_site + next_button.get("href")
            time.sleep(delay - (time.time()-load_time))
        if(self.debug):
            print("")

        return stories, i

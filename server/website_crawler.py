# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:46:05 2019

@author: Vishal Patel
"""
import urllib
from bs4 import BeautifulSoup
import json

import time

# Internal
#import parse_utils as p

class Ao3_crawler:
    base_site = "https://archiveofourown.org"
    test_fandom_list = "https://archiveofourown.org/media/Anime%20*a*%20Manga/fandoms"
    test_fandom = "https://archiveofourown.org/tags/1984%20-%20George%20Orwell/works"
    def __init__(self):
        self.fandoms = set()
        self.urls = set()
        
        #fandom_page_count = {}
        
        for url in Ao3_crawler.parse_one_fandom_list(Ao3_crawler.test_fandom_list):
            self.fandoms.add(url)
        pages_read = 0
        for fandom in self.fandoms:
            print("("+str(pages_read)+") Reading", fandom[0], "Fandom Page:", end = " ")
            fandom_url = fandom[1]
            stories, result_pages = Ao3_crawler.parse_one_fandom(fandom_url, delay=0.75)
            print("\thas", len(stories), "stories and", result_pages, "page(s) of results.")
            pages_read += result_pages
            for url in stories:
                self.urls.add(url)
    
    def toJson(self):
        print("TO JSON")
        d = {}
        d["base_site"] = Ao3_crawler.base_site
        d["fandoms"] = list(self.fandoms)
        d["stories"] = list(self.urls)
        return json.dumps(d, indent=2)
    
    def parse_one_fandom_list(fandom_list_url):
        fandoms = []
        
        page = urllib.request.urlopen(fandom_list_url)
        html = BeautifulSoup(page, 'html.parser')
        inner_main = html.find('div', {'id':'main'})
        
        fandom_index = inner_main.find('ol', {'class':'alphabet fandom index group'})
        #print(str(fandom_index)[:1000])
        letter_boxes = fandom_index.find_all('li',{"class":'letter listbox group'})
        print('Reading Boxes:', end=" ")
        for lb in letter_boxes:
            print(lb.get('id')[-1], end = " ")
            name_boxes = lb.find('ul', {'class':'tags index group'}).find_all('li')
            for nb in name_boxes:
                x = nb.find('a')
                fandoms.append( (x.text, Ao3_crawler.base_site+x.get('href')) )
        print("")
        print("")
        
        return fandoms
    
    def parse_one_fandom(fandom_page_1_url, delay = 1):
        curr_page_url = fandom_page_1_url
        urls = []
        i = 0
        #print('\t\tReading Page:', end=" ")
        while True:
            i+=1
            print(i, end = " ")#curr_page_url)
            
            # Load and read page
            loaded = False
            while not loaded:
                try:
                    page = urllib.request.urlopen(curr_page_url)
                    load_time = time.time()
                    loaded = True
                except:
                    loaded = False
            
            html = BeautifulSoup(page, 'html.parser')
            inner_main = html.find('div', {'id':'main'})
            
            #Collect URLs
            info_boxes = inner_main.find_all('li', {'class':'work blurb group', 'role':'article'})
            for ib in info_boxes:
                title_box = ib.find('h4', {'class':'heading'})
                title = title_box.find('a')
                urls.append( (title.text, Ao3_crawler.base_site+title.get("href")) )
            
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
            time.sleep(time.time()-load_time)
        print("")
        
        return urls, i

def test():
    Ao3_json = Ao3_crawler().toJson()
    with open('test_json.json', 'w') as f:
        f.write(Ao3_json)
    #print(Ao3_json[:1000])
    
    #Ao3_data = json.loads(Ao3_json)
    #pprint.pprint(Ao3_data)

test()
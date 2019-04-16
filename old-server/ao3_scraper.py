import urllib
from bs4 import BeautifulSoup
import json
import pprint
# Internal
import parse_utils as p

class Ao3_Story():
    """docstring for Ao3_Story."""

    site_url = "https://archiveofourown.org"

    def tag_strip(tag_dd_section):
        if tag_dd_section is None:
            return []
        else:
            return [str(x.text) for x in tag_dd_section.find_all('li')]
    
    def dd_find(info_box, name):
        return info_box.find('dd', {"class":name})

    def __init__(self, story_url):
        super(Ao3_Story, self).__init__()
        page = urllib.request.urlopen(story_url)
        html = BeautifulSoup(page, 'html.parser')

        # By pass adult content warning if necessary
        y = html.find('a', text="Proceed")
        if y is not None:
            url = y.get('href')
            story_url = Ao3_Story.site_url + url
            page = urllib.request.urlopen(story_url)
            html = BeautifulSoup(page, 'html.parser')

        # Extract Story Tags
        x = html.find(id='main')
        x = x.find('div', {"class":"work"})
        info_box = x.find('div', {"class":"wrapper"})

        self.rating         = Ao3_Story.dd_find(info_box, "rating tags")
        self.fandoms        = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, "fandom tags"))
        self.characters     = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'character tags'))
        self.relationships  = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'relationship tags'))
        self.categories     = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'category tags'))
        self.other_tags     = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'freeform tags'))
        self.warnings       = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'warning tags'))
        self.language       = Ao3_Story.dd_find(info_box, "language")
        
        self.publish_date   = Ao3_Story.dd_find(info_box, "published")
        self.status         = p.clean_string(info_box.find('dt', {"class":"status"}).text)[:-1]
        self.update_date    = Ao3_Story.dd_find(info_box, "status")
        self.word_count     = int(Ao3_Story.dd_find(info_box, "words").text)
        self.chapter_count  = int(Ao3_Story.dd_find(info_box, "chapters").text.split("/")[0])
        self.comment_count  = int(Ao3_Story.dd_find(info_box, "comments").text)
        self.kudo_count     = int(Ao3_Story.dd_find(info_box, "kudos").text)
        self.bookmark_count = int(Ao3_Story.dd_find(info_box, "bookmarks").text)
        self.hit_count      = int(Ao3_Story.dd_find(info_box, "hits").text)

        # Extract Title/Author
        content_box = x.find('div', id='workskin')
        self.title = content_box.find('h2', {'class':'title heading'})
        self.author = content_box.find('a', {'rel':'author'})

    def toDict(self):
        d = {}
        d['title']          = p.clean_string(self.title.text)
        d['author']         = p.clean_string(self.author.text)
        d['rating']         = p.clean_string(self.rating.text)
        d['warnings']       = self.warnings
        d['categories']     = self.categories
        d['fandoms']        = self.fandoms
        d['characters']     = self.characters
        d['relationships']  = self.relationships
        d['other_tags']     = self.other_tags
        d['language']       = p.clean_string(self.language.text)
        d['publish date']   = p.clean_string(self.publish_date.text)
        d['status']         = self.status
        d['update date']    = p.clean_string(self.update_date.text)
        d['word count']     = self.word_count
        d['chapter count']  = self.chapter_count
        d['kudo count']     = self.kudo_count
        d['bookmark count'] = self.bookmark_count
        d['comment count']  = self.comment_count
        
        return d

    def toJson(self):
        return json.dumps(self.toDict())

def ao3_scaper_test():
    test_urls = ["https://archiveofourown.org/works/4265619/chapters/9657279" # Has Explicit Content Warning
                ,"https://archiveofourown.org/works/12805206/chapters/29490435#workskin" # Has many characters
                ,"https://archiveofourown.org/works/12088434/chapters/31821954" # Multiple Fandoms
                , "https://archiveofourown.org/works/5111873/chapters/14271274"
                , "https://archiveofourown.org/works/13521369/chapters/31015518"
                , "https://archiveofourown.org/works/15343806/chapters/35686365"
                ]

    for url in test_urls:
        #Ao3_Story(url)
        pprint.pprint(
            json.loads( Ao3_Story(url).toJson() )
        )

ao3_scaper_test()

import urllib
from bs4 import BeautifulSoup
import json
from datetime import date

# Internal
import story_search.parse_utils as p
#import parse_utils as p

class Ao3_Story():
    """docstring for Ao3_Story."""

    base_site = "https://archiveofourown.org"

    def tag_strip(tag_dd_section):
        if tag_dd_section is None:
            return []
        else:
            return [str(x.text) for x in tag_dd_section.find_all('li')]
    def num_strip(num_section):
        if num_section is None:
            return 0
        else:
            return int(num_section.text)

    def dd_find(info_box, name):
        return info_box.find('dd', {"class":name})

    def __init__(self, story_url):
        super(Ao3_Story, self).__init__()
        page = urllib.request.urlopen(story_url)
        html = BeautifulSoup(page, 'html.parser')
        outer = html.find('div', id='outer')

        # By pass adult content warning if necessary
        y = outer.find('a', text="Proceed")
        curr_url = story_url
        while y is not None:
            #print('Bypassing')
            curr_url = Ao3_Story.base_site + y.get('href')
            page = urllib.request.urlopen(curr_url)
            html = BeautifulSoup(page, 'html.parser')
            outer = html.find('div', id='outer')
            y = outer.find('a', text="Proceed")

        #print('Bypassed')


        # Extract Story Tags
        x = outer.find(id='main')
        #print(str(x)[:5000])
        z = x.find('div', {"class":"work"})
        if z is not None:
            info_box = z.find('div', {"class":"wrapper"})
            if info_box is None:
                info_box = x.find('div', {"class":"wrapper"})
        else:
            info_box = x.find('div', {"class":"wrapper"})
        if info_box is None:
            raise ValueError("Could not find Info Box")

        self.rating         = p.clean_string(Ao3_Story.dd_find(info_box, "rating tags").text)
        self.fandoms        = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, "fandom tags"))
        self.characters     = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'character tags'))
        self.relationships  = [p.read_relationship(x) for x in Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'relationship tags'))]
        self.categories     = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'category tags'))
        self.other_tags     = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'freeform tags'))
        self.warnings       = Ao3_Story.tag_strip(Ao3_Story.dd_find(info_box, 'warning tags'))
        self.language       = p.clean_string(Ao3_Story.dd_find(info_box, "language").text)

        self.publish_date   = p.read_date(Ao3_Story.dd_find(info_box, "published").text)
        update_date_box = Ao3_Story.dd_find(info_box, "status")
        if update_date_box is not None:
            self.update_date= p.read_date(Ao3_Story.dd_find(info_box, "status").text)
            self.status     = p.clean_string(info_box.find('dt', {"class":"status"}).text)[:-1]
        else:
            self.status     = "Completed"
            self.update_date= self.publish_date
        self.word_count     = Ao3_Story.num_strip(Ao3_Story.dd_find(info_box, "words"))
        self.chapter_count  = int(Ao3_Story.dd_find(info_box, "chapters").text.split("/")[0])
        self.comment_count  = Ao3_Story.num_strip(Ao3_Story.dd_find(info_box, "comments"))
        self.kudo_count     = Ao3_Story.num_strip(Ao3_Story.dd_find(info_box, "kudos"))
        self.bookmark_count = Ao3_Story.num_strip(Ao3_Story.dd_find(info_box, "bookmarks"))
        self.hit_count      = Ao3_Story.num_strip(Ao3_Story.dd_find(info_box, "hits"))

        # Extract Title/Author
        content_box = x.find('div', id='workskin')
        self.title = p.clean_string(content_box.find('h2', {'class':'title heading'}).text)
        author_box = content_box.find('a', {'rel':'author'})
        if author_box is None:
            self.author = {"name":'Anonymous', 'url':''}
        else:
            self.author = {'name':p.clean_string(author_box.text), 'url':Ao3_Story.base_site+author_box.get('href')}

        # Get Chapter titles and urls
        chapter_select = x.find('select', id='selected_id')
        if chapter_select is not None:
            self.chapters = []
            for chapter in chapter_select.find_all('option'):
                chapter_number, chapter_title = chapter.text.split(" ", 1)
                chapter_number = int(chapter_number[:-1])
                chapter_url = story_url + '/chapters/' + chapter.get('value')
                self.chapters.append({'title':chapter_title,
                                      'number':chapter_number,
                                      'url':chapter_url})
            assert(len(self.chapters) == self.chapter_count)
        else:
            self.chapters = [{'title':'', 'number':1, 'url':curr_url}]

    def toDict(self):
        d = {}
        d['title']          = self.title
        d['author']         = self.author
        d['rating']         = self.rating
        d['warnings']       = self.warnings
        d['categories']     = self.categories
        d['fandoms']        = self.fandoms
        d['characters']     = self.characters
        d['relationships']  = self.relationships
        d['other_tags']     = self.other_tags
        d['language']       = self.language
        d['publish date']   = self.publish_date
        d['status']         = self.status
        d['update date']    = self.update_date
        d['word count']     = self.word_count
        d['chapter count']  = self.chapter_count
        d['chapters']       = self.chapters
        d['kudo count']     = self.kudo_count
        d['bookmark count'] = self.bookmark_count
        d['comment count']  = self.comment_count

        return d

    def toJson(self):
        return json.dumps(self.toDict(), indent=2)

class FFnet_Story():
    """docstring for FFnet_Scraper."""

    def __init__(self, story_url):
        super(FFnet_Story, self).__init__()
        page = urllib.request.urlopen(story_url)
        html = BeautifulSoup(page, 'html.parser')
        info_box = html.find(id='profile_top')

        self.title = info_box.find('b', attrs={'class':'xcontrast_txt'})
        self.author = info_box.find_all('a', attrs={'class':'xcontrast_txt'}, limit=1)[0]

        self.summary = info_box.find(attrs={'style':'margin-top:2px','class':'xcontrast_txt'})

        otherInfo = info_box.find_all('span', attrs={'class':'xgray xcontrast_txt'})[0]
        infoStrings = otherInfo.getText().split(' - ')
        i = 0;

        self.maturity_rating, i             = p.strip_label(infoStrings[i], "Rated: ", i, p.clean_string)
        self.language, i                    = p.strip_label(infoStrings[i], "", i)
        self.genres, i                      = p.strip_label(infoStrings[i], "", i, lambda x: x.split('/'), [])
        (self.characters, self.romances), i = p.strip_label(infoStrings[i], "", i, p.read_character_string, [])
        self.chapter_count, i               = p.strip_label(infoStrings[i], "Chapters: ", i, p.read_int, 1)
        self.word_count, i                  = p.strip_label(infoStrings[i], "Words: ", i, p.read_int, 0)

        self.review_count, i                = p.strip_label(infoStrings[i], "Reviews: ", i, p.read_int, 0)
        self.fav_count, i                   = p.strip_label(infoStrings[i], "Favs: ", i, p.read_int, 0)
        self.follow_count, i                = p.strip_label(infoStrings[i], "Follows: ", i, p.read_int, 0)
        self.update_date, i                 = p.strip_label(infoStrings[i], "Updated: ", i)
        self.pub_date, i                    = p.strip_label(infoStrings[i], "Published: ", i)
        self.status, i                      = p.strip_label(infoStrings[i], "Status: ", i)
        self.story_id, i                    = p.strip_label(infoStrings[i], "id: ", i, int, -1)

    def print(self):
        print(self.title.string, "by:", self.author.string)
        print(self.summary.string)
        print("Rating:", self.maturity_rating, "Lang:", self.language,"Genres:", self.genres)
        print("Characters:", self.characters)
        print("Romances:", self.romances)
        print("Chapters:", self.chapter_count, "Words:", self.word_count)
        print("Reviews:", self.review_count, "Favs:", self.fav_count, "Follows:", self.follow_count)
        print("Published:", self.pub_date, "Updated:", self.update_date)
        print("FFnet Story ID", self.story_id)
        print("")

    def toDict(self):
        d = {}
        d["title"]       = self.title.string
        d["author"]      = self.author.string
        d["rating"]      = self.maturity_rating
        d["language"]    = self.language
        d["genres"]      = self.genres
        d["characters"]  = self.characters
        d["romances"]    = self.romances
        d["chapters"]    = self.chapter_count
        d["word_count"]  = self.word_count
        d["reviews"]     = self.review_count
        d["favs"]        = self.fav_count
        d["follows"]     = self.follow_count
        d["published"]   = self.pub_date
        d["updated"]     = self.update_date
        d["id"]          = self.story_id
        return d

    def toJson(self):
        return json.dumps(self.toDict())
    def toInsertQuery(self, table_name):
        #TODO: FIX THIS
        # FROM: https://stackoverflow.com/questions/9336270/using-a-python-dict-for-a-sql-insert-statement
        myDict = self.toDict()
        columns_string  = "('" + "','".join(myDict.keys()) + "')"
        values_string   = '('+','.join(map(str,myDict.values()))+')'
        sql = """INSERT INTO %s %s VALUES %s"""%(table_name, columns_string,values_string)
        return sql

if __name__ == "__main__":
    if(True):
        print('Testing Ao3 Scraper')
        test_urls = ["https://archiveofourown.org/works/4265619/" # Has Explicit Content Warning
                    ,"https://archiveofourown.org/works/12805206/" # Has many characters
                    ,"https://archiveofourown.org/works/12088434/" # Multiple Fandoms
                    , "https://archiveofourown.org/works/5111873/"
                    , "https://archiveofourown.org/works/13521369/"
                    , "https://archiveofourown.org/works/15343806/"
                    ]

        for url in test_urls:
            #Ao3_Story(url)
            print(Ao3_Story(url).toJson())
    if(False):
        print('Testing FFnet Scraper')
        test_urls = ["https://www.fanfiction.net/s/12606073/39/"
                    ,"https://www.fanfiction.net/s/8640725/1/Game-Over"
                    ,"https://www.fanfiction.net/s/12590747/11/"
                    ,"https://www.fanfiction.net/s/10025439/25/"
                    ]

        for url in test_urls:
            print(FFnet_Story(url).toJson())

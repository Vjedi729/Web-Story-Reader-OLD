import urllib
from bs4 import BeautifulSoup
import json
from datetime import date

# Internal
import story_search.parse_utils as p

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

        self.publish_date   = p.read_date(Ao3_Story.dd_find(info_box, "published").text)
        self.status         = p.clean_string(info_box.find('dt', {"class":"status"}).text)[:-1]
        self.update_date    = p.read_date(Ao3_Story.dd_find(info_box, "status").text)
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
        d['publish date']   = self.publish_date
        d['status']         = self.status
        d['update date']    = self.update_date
        d['word count']     = self.word_count
        d['chapter count']  = self.chapter_count
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
    print('Testing Ao3 Scraper')
    test_urls = ["https://archiveofourown.org/works/4265619/chapters/9657279" # Has Explicit Content Warning
                ,"https://archiveofourown.org/works/12805206/chapters/29490435#workskin" # Has many characters
                ,"https://archiveofourown.org/works/12088434/chapters/31821954" # Multiple Fandoms
                , "https://archiveofourown.org/works/5111873/chapters/14271274"
                , "https://archiveofourown.org/works/13521369/chapters/31015518"
                , "https://archiveofourown.org/works/15343806/chapters/35686365"
                ]

    for url in test_urls:
        #Ao3_Story(url)
        print(Ao3_Story(url).toJson())

    print('Testing FFnet Scraper')
    test_urls = ["https://www.fanfiction.net/s/12606073/39/"
                ,"https://www.fanfiction.net/s/8640725/1/Game-Over"
                ,"https://www.fanfiction.net/s/12590747/11/"
                ,"https://www.fanfiction.net/s/10025439/25/"
                ]

    for url in test_urls:
        print(FFnet_Story(url).toJson())

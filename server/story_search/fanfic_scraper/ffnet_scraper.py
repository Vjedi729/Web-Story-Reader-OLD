import urllib
from bs4 import BeautifulSoup
import json

import parse_utils as p

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

def test():
    test_urls = ["https://www.fanfiction.net/s/12606073/39/"
                ,"https://www.fanfiction.net/s/8640725/1/Game-Over"
                ,"https://www.fanfiction.net/s/12590747/11/"
                ,"https://www.fanfiction.net/s/10025439/25/"
                ]
    
    for url in test_urls:
        print(FFnet_Story(url).toJson())

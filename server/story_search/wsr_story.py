# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 13:47:12 2019

@author: Vishal Patel
"""
import json
import enum
from datetime import date

from django.db.models import Count, Q

from .models import Author, Fandom, Story, Relationship, Tag, Character, Chapter
import story_search.parse_utils

class StoryType(enum.Enum):
    FFnet   = 0
    Ao3     = 1
    DB      = 2

class WSR_Story:
    def from_FFnet(self, story):
        self.title          = story.title
        self.author         = {'ffnet':story.author}
        self.rating         = story.maturity_rating
        self.language       = story.language
        self.status         = story.status
        # Tags
        self.fandoms        = story.fandoms
        self.characters     = story.characters
        self.relationships  = story.romances
        self.other_tags     = story.genres
        # Lengths
        self.word_count     = story.word_count
        self.chapter_count  = story.chapter_count
        self.chapters       = [] # TODO: Fix this!
        # Upload Info
        self.publish_date   = story.publish_date
        self.update_date    = story.update_date
        # Interactions
        self.like_count     = story.fav_count
        self.follow_count   = story.follow_count
        self.comment_count  = story.review_count
        pass

    def from_Ao3(self, story):
        self.title          = story.title
        self.author         = {'ao3':story.author}
        self.rating         = story.rating
        self.language       = story.language
        self.status         = story.status
        # Tags
        self.fandoms        = story.fandoms
        self.characters     = story.characters
        self.relationships  = story.relationships
        self.other_tags     = story.other_tags + story.categories + story.warnings
        # Lengths
        self.word_count     = story.word_count
        self.chapter_count  = story.chapter_count
        self.chapters       = story.chapters
        # Upload Info
        self.publish_date   = story.publish_date
        self.update_date    = story.update_date
        # Interactions
        self.like_count     = story.kudo_count
        self.follow_count   = story.bookmark_count
        self.comment_count  = story.comment_count

    def from_DB(self, story):
        self.id             = story.pk
        self.title          = str(story.title)
        self.author         = str(story.author)
        self.rating         = str(story.rating)
        self.language       = str(story.language)
        self.status         = str(story.status)
        # Tags
        self.fandoms        = [fandom.name for fandom in story.fandoms.all()]
        self.characters     = [char.name for char in story.characters.all()]
        self.relationships  = [[char.name for char in r.characters.all()] for r in story.relationships.all()]
        self.other_tags     = [tag.tag for tag in story.other_tags.all()]
        # Lengths
        self.word_count     = story.word_count
        self.chapter_count  = story.chapter_count
        #self.chapters       = [story.chapter_set.all()]
        # Upload Info
        self.publish_date   = story.publish_date
        self.update_date    = story.update_date
        # Interactions
        self.like_count     = story.like_count
        self.follow_count   = story.follow_count
        self.comment_count  = story.comment_count
        pass

    def __init__(self, story_type, story):
        self.id = None
        self.story_type = story_type
        if story_type == StoryType.FFnet:
            self.from_FFnet(story)
        elif story_type == StoryType.Ao3:
            self.from_Ao3(story)
        elif story_type == StoryType.DB:
            self.from_DB(story)
        else:
            raise ValueError("Story Type Not Recognized:" + str(story_type))

    def toDict(self):
        d = {}
        if self.id is not None:
            d['story_id'] = self.id
        # Basic Information
        d['title']          = self.title
        d['author']         = self.author
        d['rating']         = self.rating
        d['language']       = self.language
        # Tags
        d['fandoms']        = self.fandoms
        d['characters']     = self.characters
        d['relationships']  = self.relationships
        d['other tags']     = self.other_tags
        # Lengths
        d['word_count']     = self.word_count
        d['chapter_count']  = self.chapter_count
        # Upload Information
        d['publish date']   = str(self.publish_date)
        d['update date']    = str(self.update_date)
        # Interactions
        d['likes']          = self.like_count
        d['follows']        = self.follow_count
        d['comments']       = self.comment_count
        return d

    def toJson(self, indent = None):
        return json.dumps(self.toDict(), indent=indent)

    def saveToDB(self):
        ao3 = self.author.get('ao3')
        if ao3 is not None:
            try:
                author = Author.objects.get(ao3_username__exact=ao3.get('name'), ao3_userlink__exact=ao3.get('url'))
            except Author.DoesNotExist:
                author = Author(ao3_username=ao3.get('name'), ao3_userlink=ao3.get('url'))
            author.save()
        else:
            ffnet = self.author.get('ffnet')
            if ffnet is not None:
                try:
                    author = Author.objects.get(ffnet_username__exact=ffnet.get('name'))
                except Author.DoesNotExist:
                    author = Author(ffnet_username=ffnet.get('name'))
                author.save()
            else:
                author = Author()
        try:
            s = Story.objects.get(title__exact = self.title, author=author)
            s.rating=self.rating
            s.language=self.language
            s.word_count = self.word_count
            s.chapter_count = self.chapter_count
            s.publish_date = self.publish_date
            s.update_date = self.update_date
            s.status = self.status
            s.like_count = self.like_count
            s.follow_count = self.follow_count
            s.comment_count = self.comment_count
        except Story.DoesNotExist:
            s = Story(
                title=self.title, author=author, rating=self.rating, language=self.language,
                word_count = self.word_count, chapter_count = self.chapter_count,
                publish_date = self.publish_date, update_date = self.update_date, status = self.status,
                like_count = self.like_count, follow_count = self.follow_count, comment_count = self.comment_count
            )
        s.save()

        # Tags
        fandom = -1
        for f_name in self.fandoms:
            try:
                dbFandom = Fandom.objects.get(name__exact=f_name)
            except:
                dbFandom = Fandom(name=f_name)
                dbFandom.save()
            finally:
                if fandom is -1:
                    fandom = dbFandom
                else:
                    fandom = None
                s.fandoms.add(dbFandom)
        for c_name in self.characters:
            try:
                dbChar = Character.objects.get(name__exact=c_name)
            except:
                if fandom is not None:
                    dbChar = Character(name=c_name, fandom=fandom)
                else:
                    dbChar = Character(name=c_name)
                dbChar.save()
            finally:
                s.characters.add(dbChar)
        #TODO: Add Relationships
        for r_names in self.relationships:
            #print(r_names)
            dbChars = []
            for c_name in r_names:
                try:
                    dbChar = Character.objects.get(name__exact=c_name)
                except:
                    if fandom is not None:
                        dbChar = Character(name=c_name, fandom=fandom)
                    else:
                        dbChar = Character(name=c_name)
                    dbChar.save()
                finally:
                    dbChars.append(dbChar)
            #print(dbChars)
            cand_rel = Relationship.objects.annotate(c=Count('characters')).filter(c=len(dbChars))
            for character in dbChars:
                if cand_rel.count() <= 0:
                    break
                cand_rel = cand_rel.filter(characters = character)

            if cand_rel.count() > 0:
                dbRel = cand_rel[0]
            else:
                dbRel = Relationship()
                dbRel.save()
                for character in dbChars:
                    dbRel.characters.add(character)
            dbRel.save()
            s.relationships.add(dbRel)
        for tag in self.other_tags:
            try:
                dbTag = Tag.objects.get(tag__exact=f_name)
            except:
                dbTag = Tag(tag=f_name)
                dbTag.save()
            finally:
                s.other_tags.add(dbTag)

        # Chapters
        for chapter in self.chapters:
            dbChapter = Chapter(story = s, number = chapter.get('number'), title = chapter.get('title'), url = chapter.get('url'))
            dbChapter.save()

        return

class WSR_Story_Query:
    def __init__(self, query_dict):
        self.Q = Q()
        self.query = query_dict
        self.Q &= WSR_Story_Query.load_title(query_dict, 'title')
        self.Q &= WSR_Story_Query.load_author(query_dict, 'author')
        self.Q &= WSR_Story_Query.load_wc(query_dict, 'word_count')
        self.Q &= WSR_Story_Query.load_chap_c(query_dict, 'chapter_count')
        self.Q &= WSR_Story_Query.load_pd(query_dict, 'publish_date')
        self.Q &= WSR_Story_Query.load_ud(query_dict, 'update_date')
        self.Q &= WSR_Story_Query.load_lc(query_dict, 'like_count')
        self.Q &= WSR_Story_Query.load_fc(query_dict, 'follow_count')
        self.Q &= WSR_Story_Query.load_cc(query_dict, 'comment_count')

    def get_stories(self):
        return Story.objects.filter(self.Q)

    def load_title(d, name):
        x = d.get(name)
        if x is not None:
            t = d.get(name+'_type')
            if t is None:
                raise ValueError("Text Feild "+name+" is missing a type field")
            if t == 'CONTAINS':
                return Q(title__contains=x)
            elif t ==  'EXACT':
                return Q(title__exact=x)
            else:
                raise ValueError("Operator "+t+" is not a valid type (Try \"CONTAINS\" or \"EXACT\")")
        else:
            return Q()
    def load_author(d, name):
        x = d.get(name)
        if x is not None:
            t = d.get(name+'_type')
            if t is None:
                raise ValueError("Text Feild "+name+" is missing a type field")
            if t == 'CONTAINS':
                a_auth = Author.objects.filter(ao3_username__contains=x)
                f_auth = Author.objects.filter(ffnet_username__contains=x)
                q = Q()
                for a in a_auth:
                    q |= Q(author=a)
                for f in f_auth:
                    q |= Q(author=f)
                return q

            elif t ==  'EXACT':
                a_auth = Author.objects.filter(ao3_username__exact=x)
                f_auth = Author.objects.filter(ffnet_username__exact=x)
                q = Q()
                for a in a_auth:
                    q |= Q(author=a)
                for f in f_auth:
                    q |= Q(author=f)
                return q
            else:
                raise ValueError("Operator "+t+" is not a valid type (Try \"CONTAINS\" or \"EXACT\")")
        else:
            return Q()
    # TODO add tags to this
    def load_wc(d, name):
        x = d.get(name)
        if x is not None:
            t = d.get(name+'_query_type')
            if t is None or len(t) == 0:
                raise ValueError("Numeric Feild "+name+" is missing a type field")
            if t[0] == 'G':
                return Q(word_count>x)
            elif t[0] ==  'L':
                return Q(word_count<x)
            else:
                raise ValueError("Operator "+t+" for Numeric Feild "+name+" is not a valid type (Try \"GREATER\" or \"LESS\")")
        else:
            return Q()
    def load_chap_c(d, name):
        x = d.get(name)
        if x is not None:
            t = d.get(name+'_query_type')
            if t is None or len(t) == 0:
                raise ValueError("Numeric Feild "+name+" is missing a type field")
            if t[0] == 'G':
                return Q(chapter_count>x)
            elif t[0] ==  'L':
                return Q(chapter_count<x)
            else:
                raise ValueError("Operator "+t+" for Numeric Feild "+name+" is not a valid type (Try \"GREATER\" or \"LESS\")")
        else:
            return Q()
    def load_pd(d, name):
        x = d.get(name)
        if x is not None:
            x = p.read_date(x)
            t = d.get(name+'_query_type')
            if t is None or len(t) == 0:
                raise ValueError("Numeric Feild "+name+" is missing a type field")
            if t[0] == 'G':
                return Q(word_count>x)
            elif t[0] ==  'L':
                return Q(word_count<x)
            else:
                raise ValueError("Operator "+t+" for Numeric Feild "+name+" is not a valid type (Try \"GREATER\" or \"LESS\")")
        else:
            return Q()
    def load_ud(d, name):
        x = d.get(name)
        if x is not None:
            x = p.read_date(x)
            t = d.get(name+'_query_type')
            if t is None or len(t) == 0:
                raise ValueError("Numeric Feild "+name+" is missing a type field")
            if t[0] == 'G':
                return Q(update_date>x)
            elif t[0] ==  'L':
                return Q(update_date<x)
            else:
                raise ValueError("Operator "+t+" for Numeric Feild "+name+" is not a valid type (Try \"GREATER\" or \"LESS\")")
        else:
            return Q()
    def load_lc(d, name):
        x = d.get(name)
        if x is not None:
            t = d.get(name+'_query_type')
            if t is None or len(t) == 0:
                raise ValueError("Numeric Feild "+name+" is missing a type field")
            if t[0] == 'G':
                return Q(like_count>x)
            elif t[0] ==  'L':
                return Q(like_count<x)
            else:
                raise ValueError("Operator "+t+" for Numeric Feild "+name+" is not a valid type (Try \"GREATER\" or \"LESS\")")
        else:
            return Q()
    def load_fc(d, name):
        x = d.get(name)
        if x is not None:
            t = d.get(name+'_query_type')
            if t is None or len(t) == 0:
                raise ValueError("Numeric Feild "+name+" is missing a type field")
            if t[0] == 'G':
                return Q(follow_count>x)
            elif t[0] ==  'L':
                return Q(follow_count<x)
            else:
                raise ValueError("Operator "+t+" for Numeric Feild "+name+" is not a valid type (Try \"GREATER\" or \"LESS\")")
        else:
            return Q()
    def load_cc(d, name):
        x = d.get(name)
        if x is not None:
            t = d.get(name+'_query_type')
            if t is None or len(t) == 0:
                raise ValueError("Numeric Feild "+name+" is missing a type field")
            if t[0] == 'G':
                return Q(comment_count>x)
            elif t[0] ==  'L':
                return Q(comment_count<x)
            else:
                raise ValueError("Operator "+t+" for Numeric Feild "+name+" is not a valid type (Try \"GREATER\" or \"LESS\")")
        else:
            return Q()

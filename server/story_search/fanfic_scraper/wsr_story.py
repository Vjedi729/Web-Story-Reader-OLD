# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 13:47:12 2019

@author: Vishal Patel
"""
import json
import enum

class StoryType(enum.Enum):
    FFnet   = 0
    Ao3     = 1

class WSR_Story:
    '''
    Story Parts:
        Title   - String
        Author  - User Reference

    '''

    def from_FFnet(self, story):
        self.title          = story.title
        self.author         = story.author
        self.rating         = story.maturity_rating
        self.language       = story.language
        self.status         = story.status
        # Tags
        'TODO: Change tags to match database structure'
        self.fandoms        = story.fandoms
        self.genres         = story.genres
        self.characters     = story.characters
        self.relationships  = story.romances
        self.other_tags     = []
        # Lengths
        self.word_count     = story.word_count
        self.chapter_count  = story.chapter_count
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
        self.author         = story.author
        self.rating         = story.rating
        self.language       = story.language
        self.status         = story.status
        # Tags
        'TODO: Change tags to match database structure'
        self.fandoms        = story.fandoms
        self.genres         = []
        self.characters     = story.characters
        self.relationships  = story.relationships
        self.other_tags     = story.other_tags
        # Lengths
        self.word_count     = story.word_count
        self.chapter_count  = story.chapter_count
        # Upload Info
        self.publish_date   = story.publish_date
        self.update_date    = story.update_date
        # Interactions
        self.like_count     = story.kudo_count
        self.follow_count   = story.bookmark_count
        self.comment_count  = story.comment_count


    def __init__(self, story_type, story):
        if story_type == StoryType.FFnet:
            self.from_FFnet(story)
        elif story_type == StoryType.Ao3:
            self.from_Ao3(story)
        else:
            raise ValueError("Story Type Not Recognized:" + str(story_type))

    def toDict(self):
        d = {}
        # Basic Information
        d['title']          = self.title
        d['author']         = self.author
        d['rating']         = self.rating
        d['language']       = self.language
        # Tags
        d['genres']         = self.genres
        d['fandoms']        = self.fandoms
        d['characters']     = self.characters
        d['relationships']  = self.relationships
        d['other tags']     = self.other_tags

        # Lengths
        d['word_count']     = self.word_count
        d['chapter_count']  = self.chapter_count

        # Upload Information
        d['publish date']   = self.publish_date
        d['update data']    = self.update_date

        # Interactions
        d['likes']          = self.like_count
        d['follows']        = self.follow_count
        d['comments']       = self.comment_count
        return d

    def toJson(self):
        return json.dumps(self.toDict())

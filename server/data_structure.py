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
        pass
    
    def from_Ao3(self, story):
        pass
    
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
        
        # Tags
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
        return json.dumps(self.toDict)
        
# Removed temporarily
'''
class Tag:
    uid = 0
    def __init__(self, name):
        # Give a unique id (within tags)
        self.id = Tag.uid
        Tag.uid += 1

        # Insert data:
        self.name = name
'''

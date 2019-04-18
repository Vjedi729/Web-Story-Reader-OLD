from django.db import models
from django.contrib.auth.models import User

# Crawler Models
class Ao3_Fandom(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(primary_key = True)

class Ao3_Story_Tracker(models.Model):
    url = models.URLField(primary_key=True)
    last_check_date = models.DateField(auto_now=True)

# Story Model
class Author(models.Model):
    local_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ffnet_username = models.CharField(max_length=255, null=True)
    ao3_username = models.CharField(max_length=255, null=True)

class Tag(models.Model):
    tag_id = models.IntegerField()
    tag = models.CharField(max_length=255)

class Fandom(models.Model):
    fandom_id = models.IntegerField()
    fandom_name = models.CharField(max_length=255)

class Character(models.Model):
    character_id = models.IntegerField()
    name = models.CharField(max_length=255)
    fandom = models.ForeignKey(Fandom, on_delete=models.CASCADE)

class Relationship(models.Model):
    characters = models.ManyToManyField(Character)

class Story(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    # Tags
    fandoms = models.ManyToManyField(Fandom)
    characters = models.ManyToManyField(Character)
    relationships = models.ManyToManyField(Relationship)
    other_tags = models.ManyToManyField(Tag)
    # Lengths
    word_count = models.IntegerField()
    chapter_count = models.IntegerField()
    # Upload Information
    publish_date = models.DateField()
    update_date = models.DateField()
    last_check_date = models.DateTimeField(auto_now = True)
    # Interactions
    like_count = models.IntegerField()
    follow_count = models.IntegerField()
    comment_count = models.IntegerField()

class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    number = models.IntegerField()
    url = models.URLField()
    upload_date = models.DateField(null=True)

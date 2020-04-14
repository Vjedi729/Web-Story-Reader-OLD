from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Crawler Models
class Ao3_Fandom(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(primary_key = True)
    fics_scanned = models.IntegerField(Field.default = 0)

    def __str__(self):
        return str(name) + " Fandom (" + str(fics_scanned) + ")" 

class Ao3_Story_Tracker(models.Model):
    url = models.URLField(primary_key=True)
    last_check_date = models.DateField(auto_now=True)

# Story Model
class Author(models.Model):
    local_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ffnet_username = models.CharField(max_length=255, null=True, unique=True)
    ffnet_userlink = models.URLField(null = True)
    ao3_username = models.CharField(max_length=255, null=True, unique=True)
    ao3_userlink = models.URLField(null = True)

    def __str__(self):
        if self.local_user is None:
            if self.ao3_username is not None:
                return str(self.ao3_username)
            else:
                return str(self.ffnet_username)
        else:
            return str(self.local_user)


class Tag(models.Model):
    same_as = models.IntegerField(null=True)
    tag = models.CharField(max_length=255, unique=True, default="")
    def __str__(self):
        return str(self.tag)

class Fandom(models.Model):
    same_as = models.IntegerField(null=True)
    name = models.CharField(max_length=255, unique=True, default="")

    def __str__(self):
        return self.name

class Character(models.Model):
    same_as = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    fandom = models.ForeignKey(Fandom, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name) + ' from ' + str(self.fandom)

class Relationship(models.Model):
    characters = models.ManyToManyField(Character)

    def __str__(self):
        c_names = [str(char.name) for char in self.characters.all()]
        return '/'.join(c_names)

class Story(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    status = models.CharField(max_length = 16, default = 'In Progress')

    # Tags
    fandoms = models.ManyToManyField(Fandom)
    characters = models.ManyToManyField(Character)
    relationships = models.ManyToManyField(Relationship)
    other_tags = models.ManyToManyField(Tag)
    # Lengths
    word_count = models.IntegerField()
    chapter_count = models.IntegerField()
    # Upload Information
    publish_date = models.DateField(default=date.min)
    update_date = models.DateField(default=date.min)
    last_check_date = models.DateTimeField(auto_now = True)
    # Interactions
    like_count = models.IntegerField()
    follow_count = models.IntegerField()
    comment_count = models.IntegerField()

    def __str__(self):
        return self.title + " by: " + str(self.author)

class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    number = models.IntegerField()
    title = models.CharField(max_length=255, null=True)
    url = models.URLField()
    upload_date = models.DateField(null=True)

    class Meta:
        unique_together = ('story', 'number')

# Read Record Model
class Read_Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.CharField(choices=[("DROP","Dropped"), ("TO_READ","To Read"), ("MARK_READ",'Read')], max_length = 10)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    read_time = models.DateTimeField(auto_now=True)

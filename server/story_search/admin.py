from django.contrib import admin
from .models import Story, Ao3_Story_Tracker, Ao3_Fandom, Relationship, Read_Record

# Register your models here.
admin.site.register(Story)
admin.site.register(Ao3_Story_Tracker)
admin.site.register(Ao3_Fandom)
admin.site.register(Relationship)
admin.site.register(Read_Record)

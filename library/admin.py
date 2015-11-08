from django.contrib import admin

from .models import Maker, Label, Series, Director, Tag, Actress, Video 

admin.site.register(Maker)
admin.site.register(Label)
admin.site.register(Series)
admin.site.register(Director)
admin.site.register(Tag)
admin.site.register(Actress)
admin.site.register(Video)

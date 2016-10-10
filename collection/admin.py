from django.contrib import admin
from .models import *

a="""
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    raw_id_fields = ("video",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("makers", "labels", "series", "directors", "actresses", "keywords", "videos", "items")
"""

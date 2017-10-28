from django.db import models
from django.contrib.auth.models import User
from library.models import *

class FileItem(models.Model):

    video = models.OneToOneField(Video, on_delete=models.CASCADE)

    filesize = models.PositiveIntegerField('size (MB)', null=True, blank=True)
    height = models.PositiveIntegerField(null=True,  blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)

    OTHER = 0
    MP4 = 1
    MKV = 2
    AVI = 3
    WMV = 4
    ISO = 5
    RMVB = 6

    CONTAINERS = (
        (OTHER, 'Others'),
        (MP4, '.mp4'),
        (MKV, '.mkv'),
        (AVI, '.avi'),
        (WMV, '.wmv'),
        (RMVB, '.rmvb'),
        (ISO, 'Disc Image'),
    )

    container = models.PositiveIntegerField(choices=CONTAINERS, default=OTHER)

    has_watermarks = models.BooleanField()
    has_subtitles = models.BooleanField()
    has_adverts = models.BooleanField()

    parts = models.PositiveIntegerField(default=1)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.video.vid


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    makers = models.ManyToManyField(Maker, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    series = models.ManyToManyField(Series, blank=True)
    directors = models.ManyToManyField(Director, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    actresses = models.ManyToManyField(Actress, blank=True)

    videos = models.ManyToManyField(Video, blank=True)
    items = models.ManyToManyField(FileItem, blank=True)

    def __str__(self):
        return self.user.username

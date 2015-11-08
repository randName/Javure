from django.db import models

class Article(models.Model):
    _id = models.PositiveIntegerField( 'ID', primary_key=True )
    name = models.CharField( max_length=20 )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['_id']

class Maker(Article):
    url = models.URLField( 'URL', blank=True )

class Director(Article):
    pass

class Label(Article):
    pass

class Series(Article):

    class Meta:
        verbose_name_plural = 'series'

class Tag(Article):

    MISC = 5
    SITUATION = 0
    ATYPE = 1
    COSTUME = 2
    GENRE = 3
    PLAY = 4

    CATEGORIES = (
        (MISC, 'Others'),
        (SITUATION, 'Situation'),
        (ATYPE, 'Actress Type'),
        (COSTUME, 'Costume'),
        (GENRE, 'Genre'),
        (PLAY, 'Play'),
    )

    category = models.PositiveIntegerField( choices=CATEGORIES, default=MISC )

class Actress(Article):

    roma = models.CharField( 'ローマ字', max_length=50, blank=True )
    furi = models.CharField( '振り仮名', max_length=50, blank=True )

    class Meta:
        verbose_name_plural = 'actresses'

class Video(models.Model):

    cid = models.CharField( 'ID', primary_key=True, max_length=20 )
    released_date = models.DateField( 'Released Date' )
    runtime = models.DurationField()
    title = models.TextField()
    display_id = models.SlugField( 'Display ID', max_length=20 )

    maker = models.ForeignKey( 'Maker' )
    director = models.ForeignKey( 'Director', blank=True, null=True )
    label = models.ForeignKey( 'Label', blank=True, null=True )
    series = models.ForeignKey( 'Series', blank=True, null=True )
    actresses = models.ManyToManyField( 'Actress', blank=True )
    tags = models.ManyToManyField( 'Tag', blank=True )

    def __str__(self):
        return self.display_id

    class Meta:
        ordering = ['-released_date']

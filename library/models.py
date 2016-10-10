from django.db import models

class Article(models.Model):
    _id = models.PositiveIntegerField( 'ID', primary_key=True )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Maker(Article):
    name = models.CharField( max_length=40 )
    url = models.URLField( 'URL', blank=True )
    description = models.TextField( blank=True )
    roma = models.CharField( 'ローマ字', max_length=50, blank=True )

class Label(Article):
    name = models.TextField()

class Series(Article):
    name = models.TextField()

    class Meta:
        verbose_name_plural = 'series'

class Director(Article):
    name = models.CharField( max_length=30 )

class Keyword(Article):
    name = models.CharField( max_length=30 )

    SITUATION = 0
    ATYPE = 1
    COSTUME = 2
    GENRE = 3
    PLAY = 4
    MISC = 5

    CATEGORIES = (
        (SITUATION, 'Situation'),
        (ATYPE, 'Actress Type'),
        (COSTUME, 'Costume'),
        (GENRE, 'Genre'),
        (PLAY, 'Play'),
        (MISC, 'Others'),
    )

    category = models.PositiveSmallIntegerField( choices=CATEGORIES, default=MISC )

class Actress(Article):
    name = models.CharField( max_length=30 )
    roma = models.CharField( 'ローマ字', max_length=50, blank=True )
    furi = models.CharField( '振り仮名', max_length=20, blank=True )
    alias = models.CharField( '別名', max_length=50, blank=True )

    class Meta:
        verbose_name_plural = 'actresses'

class Video(models.Model):
    title = models.TextField()
    name = models.SlugField( '品番', max_length=20, blank=True, null=True )
    runtime = models.DurationField( blank=True, null=True )
    released_date = models.DateField( 'Released Date', blank=True, null=True )

    maker = models.ForeignKey( Maker, on_delete=models.PROTECT )
    label = models.ForeignKey( Label, on_delete=models.SET_NULL, blank=True, null=True )
    series = models.ForeignKey( Series, on_delete=models.SET_NULL, blank=True, null=True )
    director = models.ForeignKey( Director, on_delete=models.SET_NULL, blank=True, null=True )
    keywords = models.ManyToManyField( Keyword, blank=True )
    actresses = models.ManyToManyField( Actress, blank=True )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-released_date']

class Content(models.Model):

    cid = models.SlugField( 'Content ID' )
    pid = models.SlugField( 'Product ID' )

    DIGITAL = 0
    MONO = 1

    REALMS = (
        (DIGITAL, 'Digital'),
        (MONO, 'DVD'),
    )

    realm = models.PositiveSmallIntegerField( choices=REALMS, default=DIGITAL )
    video = models.ForeignKey( Video, on_delete=models.CASCADE )
    width = models.PositiveSmallIntegerField( default=0 )
    height = models.PositiveSmallIntegerField( default=0 )

    def __str__(self):
        return self.cid

    class Meta:
        ordering = ['realm']

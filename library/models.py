from django.db import models

class Article(models.Model):

    _id = models.PositiveIntegerField( 'ID', primary_key=True )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Maker(Article):

    name = models.CharField( max_length=50 )
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

    name = models.CharField( max_length=50 )

class Keyword(Article):

    name = models.CharField( max_length=20 )
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

    category = models.PositiveIntegerField( choices=CATEGORIES, default=MISC )

class Actress(Article):

    name = models.CharField( max_length=50 )
    roma = models.CharField( 'ローマ字', max_length=50, blank=True )
    furi = models.CharField( '振り仮名', max_length=20, blank=True )

    class Meta:
        verbose_name_plural = 'actresses'

class Video(models.Model):

    _id = models.SlugField( 'ID', primary_key=True, max_length=20 )
    released_date = models.DateField( 'Released Date' )
    runtime = models.DurationField()
    title = models.TextField()

    maker = models.ForeignKey( Maker, on_delete=models.PROTECT )
    label = models.ForeignKey( Label, on_delete=models.SET_NULL, blank=True, null=True )
    series = models.ForeignKey( Series, on_delete=models.SET_NULL, blank=True, null=True )
    director = models.ForeignKey( Director, on_delete=models.SET_NULL, blank=True, null=True )
    keywords = models.ManyToManyField( Keyword, blank=True )
    actresses = models.ManyToManyField( Actress, blank=True )

    def __str__(self):
        return self._id

    class Meta:
        ordering = ['-released_date']

class Content(models.Model):

    cid = models.SlugField( 'Content ID', primary_key=True )
    pid = models.SlugField( 'Product ID' )

    DIGITAL = 0
    MONO = 1

    REALMS = (
        (DIGITAL, 'Digital'),
        (MONO, 'DVD'),
    )

    realm = models.PositiveIntegerField( choices=REALMS, default=DIGITAL )
    video = models.ForeignKey( Video, on_delete=models.CASCADE )

    def __str__(self):
        return self.cid

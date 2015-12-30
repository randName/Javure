from django.db import models

class Article(models.Model):

    _id = models.PositiveIntegerField( 'ID', primary_key=True )
    name = models.CharField( max_length=20 )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Maker(Article):

    url = models.URLField( 'URL', blank=True )
    description = models.TextField( blank=True )
    roma = models.CharField( 'ローマ字', max_length=50, blank=True )

class Label(Article):
    pass

class Series(Article):

    class Meta:
        verbose_name_plural = 'series'

class Director(Article):
    pass

class Keyword(Article):

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

    roma = models.CharField( 'ローマ字', max_length=50, blank=True )
    furi = models.CharField( '振り仮名', max_length=20, blank=True )

    class Meta:
        verbose_name_plural = 'actresses'

class Video(models.Model):

    pid = models.SlugField( 'Product ID', primary_key=True )
    cid = models.SlugField( 'Content ID' )

    display_id = models.SlugField( 'Display ID', max_length=20 )
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
        return self.display_id

    class Meta:
        ordering = ['-released_date']

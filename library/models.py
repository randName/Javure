from django.db import models

class Article(models.Model):
    _id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['_id']

class Maker(Article):
    url = models.URLField(blank=True)

class Director(Article):
    pass

class Label(Article):
    pass

class Series(Article):

    class Meta:
        verbose_name_plural = "Series"

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

    category = models.PositiveIntegerField(choices=CATEGORIES,default=MISC)

class Actress(Article):
    roma = models.CharField(max_length=50,blank=True)
    furi = models.CharField(max_length=50,blank=True)

    class Meta:
        verbose_name_plural = "Actresses"

class Video(models.Model):
    cid = models.CharField(primary_key=True,max_length=20)
    released_date = models.DateField()
    runtime = models.DurationField()
    title = models.TextField()
    display_id = models.SlugField(max_length=20)
    maker = models.ForeignKey('Maker')
    director = models.ForeignKey('Director',blank=True,null=True)
    label = models.ForeignKey('Label',blank=True,null=True)
    series = models.ForeignKey('Series',blank=True,null=True)
    tags = models.ManyToManyField('Tag',blank=True)
    actresses = models.ManyToManyField('Actress',blank=True)

    def __str__(self):
        return self.display_id

    class Meta:
        ordering = ['-released_date']

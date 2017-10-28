from django.db import models


class Article(models.Model):
    """Base model class for articles."""
    _id = models.PositiveIntegerField('ID', primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Maker(Article):
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    roma = models.CharField('romaji', max_length=255, blank=True)


class Label(Article):
    pass


class Series(Article):

    class Meta:
        verbose_name_plural = 'series'


class Director(Article):
    pass


class Keyword(Article):

    SITUATION = 0
    ACTTYPE = 1
    COSTUME = 2
    GENRE = 3
    PLAY = 4
    MISC = 5

    CATEGORIES = (
        (SITUATION, 'Situation'),
        (ACTTYPE, 'Actress Type'),
        (COSTUME, 'Costume'),
        (GENRE, 'Genre'),
        (PLAY, 'Play'),
        (MISC, 'Others'),
    )

    category = models.PositiveSmallIntegerField(choices=CATEGORIES, default=MISC)


class Actress(Article):
    roma = models.CharField('romaji', max_length=255, blank=True)
    furi = models.CharField('furigana', max_length=255, blank=True)
    alias = models.CharField('aliases', max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'actresses'


class Video(models.Model):
    vid = models.SlugField(max_length=255, blank=True)
    title = models.TextField()
    description = models.TextField(blank=True)
    runtime = models.DurationField(blank=True, null=True)
    released_date = models.DateField(blank=True, null=True)

    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    actresses = models.ManyToManyField(Actress, blank=True)

    def __str__(self):
        return self.vid

    class Meta:
        ordering = ['-released_date']

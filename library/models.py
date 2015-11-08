from django.db import models

class Maker(models.Model):
    m_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Director(models.Model):
    d_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Label(models.Model):
    l_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Series(models.Model):
    s_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Tag(models.Model):
    t_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    MISC = 5
    SITUATION = 0
    ATYPE = 1
    COSTUME = 2
    GENRE = 3
    PLAY = 4

    TYPE_CHOICES = (
        (MISC, 'Others'),
        (SITUATION, 'Situation'),
        (ATYPE, 'Actress Type'),
        (COSTUME, 'Costume'),
        (GENRE, 'Genre'),
        (PLAY, 'Play'),
    )

    t_type = models.PositiveIntegerField(choices=TYPE_CHOICES,default=MISC)

    def __str__(self):
        return self.name

class Actress(models.Model):
    a_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    roma = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name

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


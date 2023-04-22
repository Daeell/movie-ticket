from django.db import models

# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title_korean = models.CharField(max_length=100)
    title_original = models.CharField(max_length=100)
    year = models.IntegerField()
    poster = models.URLField()
    rating_percent = models.FloatField()
    rating_average = models.FloatField()
    rating_votes = models.IntegerField()
    runtime = models.IntegerField()
    director = models.CharField(max_length=100)
    synopsis = models.TextField()

class Trailers(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trailers')
    url = models.URLField()
    type = models.CharField(max_length=50)

class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast')
    actor = models.CharField(max_length=50)
    character = models.CharField(max_length=50)
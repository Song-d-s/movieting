from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=64)

class Keyword(models.Model):
    name = models.CharField(max_length=128)

class Actor(models.Model):
    name = models.CharField(max_length=128)
    profile_path = models.CharField(max_length=128, null=True)

class Director(models.Model):
    name = models.CharField(max_length=128)
    profile_path = models.CharField(max_length=128, null=True)

class Movie(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'like_movies')
    title = models.CharField(max_length=128)
    original_title = models.CharField(max_length=128)
    release_date = models.CharField(max_length=128)
    vote_average = models.FloatField(null=True, blank=True)
    popularity = models.FloatField()
    overview = models.TextField(null=True, blank=True)
    backdrop_path = models.CharField(max_length=128)
    poster_path = models.CharField(max_length=128)
    genres = models.ManyToManyField(Genre, related_name='movie_genres')
    keywords = models.ManyToManyField(Keyword, related_name='movie_keywords')
    actors = models.ManyToManyField(Actor, related_name='movie_actors')
    directors = models.ManyToManyField(Director, related_name='movie_directors')
    vote_average_naver = models.FloatField(null=True, blank=True)
    link_naver = models.TextField(null=True, blank=True)
    youtube = models.CharField(max_length=128, null=True, blank=True)
    vote_count = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name = 'comments')
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_survey = models.IntegerField(default=0)

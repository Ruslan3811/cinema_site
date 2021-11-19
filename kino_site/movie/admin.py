from django.contrib import admin
from .models import Reviews, Rating, RatingStar, MovieShots, Movie, Genre, Actor, Category
# Register your models here.
models = [Reviews, Rating, RatingStar, MovieShots, Movie, Genre, Actor, Category]
admin.site.register(models)
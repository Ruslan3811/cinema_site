from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Movie, Reviews, Category, Actor, Genre
from .forms import ReviewForm
from django.shortcuts import redirect
import inspect
from django.db.models import Q

# Create your views here.

class GenreYear:
    """Жанры и года"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")

class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = "templates/movie/actor.html"
    slug_field = 'name'

class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    template_name = "templates/movie/movie_list.html"

    def get_queryset(self):
        #Будем фильтровать фильмы там, где года будут входить в список, который нам будет возвращаться
        queryset = Movie.objects.filter(Q(year__in = self.request.GET.getlist("year")) |
                                        Q(genres__in = self.request.GET.getlist("genre")))
        return queryset

class MoviesView(GenreYear, ListView):
    # При http get-запросе вызывается данный метод
    model = Movie
    queryset = Movie.objects.filter(draft = False)
    template_name = "templates/movie/movie_list.html"


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'
    template_name = "templates/movie/movie_detail.html"

class AddReviewView(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id = pk)
        if form.is_valid():
            form = form.save(commit=False)
            if (request.POST.get("parent", None)):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


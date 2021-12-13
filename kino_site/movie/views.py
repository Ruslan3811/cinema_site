from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Movie, Reviews, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm
from django.shortcuts import redirect
import inspect
from django.db.models import Q
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #RatingForm() - закладываем значения формы в контекст
        # Для передачи в шаблон данных. Форма должна показываться на странице!
        context["star_form"] = RatingForm()
        # print(context["star_form"])
        return context


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

class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if (form.is_valid()):
        #defaults - словарь, который необходим для обновления, movie_id и ip не будут обновляться
        # при дальнейшем изменении ip и movie_id меняться не будут
            Rating.objects.update_or_create(ip = self.get_client_ip(request),
                                            movie_id = int(request.POST.get("movie")),
                                            defaults = {'star_id': int(request.POST.get("star"))})
            movie_obj = Movie.objects.get(id=request.POST.get("movie"))
            return redirect(movie_obj.get_absolute_url())
        else:
            return HttpResponse(status=400)
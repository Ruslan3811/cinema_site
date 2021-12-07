from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Movie, Reviews, Category
from .forms import ReviewForm
from django.shortcuts import redirect
import inspect

# Create your views here.

class MoviesView(ListView):
    # При http get-запросе вызывается данный метод
    model = Movie
    queryset = Movie.objects.filter(draft = False)
    template_name = "templates/movie/movie_list.html"


class MovieDetailView(DetailView):
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


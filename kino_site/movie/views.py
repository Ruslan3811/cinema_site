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
from django.core.paginator import Paginator

# Create your views here.

class Pages:
    """Страницы"""
    def get_pages(self, context):
        p = Paginator(self.queryset, self.paginate_by)
        middle = []
        left_dot, right_dot = True, True
        if (context["page_obj"].has_previous()):
            middle.append(context["page_obj"].previous_page_number())
        if (p.num_pages > 0):
            middle.append(context["page_obj"].number)
        if (context["page_obj"].has_next()):
            middle.append(context["page_obj"].next_page_number())
        left = [x for x in range(1,3) if x not in middle]
        right = [x for x in range(p.num_pages - 1, p.num_pages + 1) if x not in middle]
        if (len(left) == 0 or (len(left) > 0 and left[-1] == middle[0] - 1)):
            left_dot = False
        if (len(right) == 0 or (len(right) > 0 and right[0] == middle[-1] + 1)):
            right_dot = False
        page_dict = {"left": left, "middle": middle, "right": right, "right_dot": right_dot, "left_dot": left_dot}
        context.update(page_dict)
        return context


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

class MoviesView(GenreYear, ListView):
    # При http get-запросе вызывается данный метод
    model = Movie
    queryset = Movie.objects.filter(draft = False)
    paginate_by = 1
    template_name = "templates/movie/movie_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context = Pages.get_pages(self, context)
        return context

class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    template_name = "templates/movie/movie_list.html"
    paginate_by = 1

    def get_queryset(self):
        #Будем фильтровать фильмы там, где года будут входить в список, который нам будет возвращаться
        queryset = Movie.objects.filter(Q(year__in = self.request.GET.getlist("year")) |
                                        Q(genres__in = self.request.GET.getlist("genre"))).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        self.queryset = self.get_queryset()
        context = Pages.get_pages(self, context)
        return context


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'
    template_name = "templates/movie/movie_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #RatingForm() - закладываем значения формы в контекст
        # Для передачи в шаблон данных. Форма должна показываться на странице!
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context


class AddReviewView(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        print("REVIEW_FORM CAME: ", form, "|\n\n\n")
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

class Search(ListView):
    model = Movie
    paginate_by = 1
    template_name = "templates/movie/movie_list.html"

    def get_queryset(self):
    #icontains - для фильтрации без учета регистра
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.queryset = self.get_queryset()
        context["title"] = f'q={self.request.GET.get("q")}&'
        context = Pages.get_pages(self, context)
        return context

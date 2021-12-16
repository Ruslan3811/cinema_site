from django.urls import path
# #
from . import views


urlpatterns = [
    path("", views.MoviesView.as_view()),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("review/<int:pk>/", views.AddReviewView.as_view(), name="review-movie"),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie-detail"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
]


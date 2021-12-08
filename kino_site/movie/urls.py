from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MoviesView.as_view(), name = "home"),
    path('filter/', views.FilterMoviesView.as_view(), name='filter'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name = 'movie-detail'),
    path('review/<int:pk>/', views.AddReviewView.as_view(), name = 'review-movie'),
    path('actors/<str:slug>/', views.ActorView.as_view(), name='actor_detail'),
]

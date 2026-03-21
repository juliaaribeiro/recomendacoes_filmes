from django.urls import path
from .views import PopularMoviesView, SearchMoviesView, MovieDetailView, TrendingMoviesView

urlpatterns = [
    path('populares/', PopularMoviesView.as_view(), name='popular_movies'),
    path('busca/', SearchMoviesView.as_view(), name='search_movies'),
    path('<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('trending/', TrendingMoviesView.as_view(), name='trending_movies'),
]
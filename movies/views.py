import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

TMDB_API_KEY = 'e85b853a307c5d0041007f7df100d1b9'  # Replace with actual key

class PopularMoviesView(APIView):
    def get(self, request):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            return Response(response.json())
        return Response({'error': 'Failed to fetch movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchMoviesView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}'
        response = requests.get(url)
        if response.status_code == 200:
            return Response(response.json())
        return Response({'error': 'Failed to search movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            return Response(response.json())
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

class TrendingMoviesView(APIView):
    def get(self, request):
        url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            return Response(response.json())
        return Response({'error': 'Failed to fetch trending movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

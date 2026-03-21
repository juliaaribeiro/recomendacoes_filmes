from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Watchlist
from .serializers import WatchlistSerializer

class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Watchlist.objects.filter(usuario=self.request.user)
        filme = self.request.query_params.get('filme')
        if filme:
            queryset = queryset.filter(filme_id=filme)
        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class WatchlistDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(usuario=self.request.user)

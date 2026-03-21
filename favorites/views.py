from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Favorito
from .serializers import FavoritoSerializer

class FavoritoListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Favorito.objects.filter(usuario=self.request.user)
        filme = self.request.query_params.get('filme')
        if filme:
            queryset = queryset.filter(filme_id=filme)
        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class FavoritoDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorito.objects.filter(usuario=self.request.user)

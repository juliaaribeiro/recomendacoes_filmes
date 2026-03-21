from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Comentario
from .serializers import ComentarioSerializer

class ComentarioListCreateView(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filme = self.request.query_params.get('filme')
        if filme:
            return Comentario.objects.filter(filme_id=filme)
        return Comentario.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class ComentarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comentario.objects.filter(usuario=self.request.user)

from django.urls import path
from .views import ComentarioListCreateView, ComentarioDetailView

urlpatterns = [
    path('', ComentarioListCreateView.as_view(), name='comentario_list'),
    path('<int:pk>/', ComentarioDetailView.as_view(), name='comentario_detail'),
]
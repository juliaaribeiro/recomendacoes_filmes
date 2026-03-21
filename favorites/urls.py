from django.urls import path
from .views import FavoritoListCreateView, FavoritoDetailView

urlpatterns = [
    path('', FavoritoListCreateView.as_view(), name='favorito_list'),
    path('<int:pk>/', FavoritoDetailView.as_view(), name='favorito_detail'),
]
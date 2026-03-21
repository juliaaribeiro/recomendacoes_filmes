from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('cadastro/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', ProfileView.as_view(), name='profile'),
]
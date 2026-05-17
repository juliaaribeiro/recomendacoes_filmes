from django.contrib import admin

from .models import Favorito

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'filme_id', 'titulo', 'poster', 'data')
    search_fields = ('usuario__email', 'titulo')
    list_filter = ('data',)

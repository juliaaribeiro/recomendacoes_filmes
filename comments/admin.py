from django.contrib import admin

from .models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'filme_id', 'titulo', 'texto', 'nota', 'data_comentario')
    search_fields = ('usuario__email', 'titulo', 'texto')
    list_filter = ('nota', 'data_comentario')

from django.contrib import admin

from .models import Watchlist

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_id', 'filme_id', 'titulo', 'assistido', 'data_adicao')
    search_fields = ('usuario__email', 'titulo')
    list_filter = ('assistido', 'data_adicao')
    list_editable = ('assistido',)  # permite editar o campo 'assistido' diretamente na listagem

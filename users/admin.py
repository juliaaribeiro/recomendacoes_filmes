from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from favorites.models import Favorito
from comments.models import Comentario
from watchlist.models import Watchlist

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'nome', 'tipo_usuario', 'is_staff', 'is_superuser', 'is_active', 'data_criacao', 'last_login')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'nome')
    ordering = ('email',)
    inlines = []
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'password1', 'password2', 'is_staff', 'is_superuser', 'tipo_usuario'),
        }),
    )


# Inlines: mostrar Favoritos / Comentários / Watchlist dentro do usuário
class FavoritoInline(admin.TabularInline):
    model = Favorito
    extra = 0
    fields = ('filme_id', 'titulo', 'data')
    readonly_fields = ('filme_id', 'titulo', 'data')


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    fields = ('filme_id', 'titulo', 'nota', 'data_comentario')
    readonly_fields = ('filme_id', 'titulo', 'nota', 'data_comentario')


class WatchlistInline(admin.TabularInline):
    model = Watchlist
    extra = 0
    fields = ('filme_id', 'titulo', 'assistido', 'data_adicao')
    readonly_fields = ('filme_id', 'titulo', 'assistido', 'data_adicao')

# Attach inlines to the registered UserAdmin
UserAdmin.inlines = [FavoritoInline, ComentarioInline, WatchlistInline]

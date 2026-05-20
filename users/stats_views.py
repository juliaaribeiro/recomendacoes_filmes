from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from comments.models import Comentario
from favorites.models import Favorito
from watchlist.models import Watchlist

User = get_user_model()

class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        agora = timezone.now()
        hoje = agora.date()
        ultimos_7_dias = agora - timedelta(days=7)
        ultimos_30_dias = agora - timedelta(days=30)

        # Usuários
        total_usuarios = User.objects.count()
        usuarios_hoje = User.objects.filter(data_criacao__date=hoje).count()
        usuarios_7_dias = User.objects.filter(data_criacao__gte=ultimos_7_dias).count()
        usuarios_30_dias = User.objects.filter(data_criacao__gte=ultimos_30_dias).count()
        usuarios_ativos = User.objects.filter(last_login__gte=ultimos_7_dias).count()

        # Cadastros por dia (últimos 7 dias)
        cadastros_por_dia = []
        for i in range(6, -1, -1):
            dia = agora - timedelta(days=i)
            count = User.objects.filter(data_criacao__date=dia.date()).count()
            cadastros_por_dia.append({
                'dia': dia.strftime('%d/%m'),
                'total': count
            })

        # Comentários
        total_comentarios = Comentario.objects.count()
        comentarios_hoje = Comentario.objects.filter(data_comentario__date=hoje).count()
        comentarios_7_dias = Comentario.objects.filter(data_comentario__gte=ultimos_7_dias).count()
        notas = list(Comentario.objects.values_list('nota', flat=True))
        notas_validas = [nota for nota in notas if nota is not None]
        media_nota_valor = round(sum(notas_validas) / len(notas_validas), 1) if notas_validas else 0

        # Favoritos
        total_favoritos = Favorito.objects.count()
        favoritos_7_dias = Favorito.objects.filter(data__gte=ultimos_7_dias).count()

        # Watchlist
        total_watchlist = Watchlist.objects.count()
        assistidos = Watchlist.objects.filter(assistido=True).count()

        # Filmes mais favoritados
        from django.db.models import Count
        filmes_favoritos = (
            Favorito.objects
            .values('filme_id', 'titulo')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )

        # Filmes mais comentados
        filmes_comentados = (
            Comentario.objects
            .values('filme_id', 'titulo')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )

        # Usuários recentes
        usuarios_recentes = list(
            User.objects
            .order_by('-data_criacao')[:5]
            .values('id', 'email', 'nome', 'data_criacao', 'last_login', 'tipo_usuario')
        )

        return Response({
            'usuarios': {
                'total': total_usuarios,
                'hoje': usuarios_hoje,
                'ultimos_7_dias': usuarios_7_dias,
                'ultimos_30_dias': usuarios_30_dias,
                'ativos_semana': usuarios_ativos,
                'cadastros_por_dia': cadastros_por_dia,
                'recentes': usuarios_recentes,
            },
            'comentarios': {
                'total': total_comentarios,
                'hoje': comentarios_hoje,
                'ultimos_7_dias': comentarios_7_dias,
                'media_nota': media_nota_valor,
            },
            'favoritos': {
                'total': total_favoritos,
                'ultimos_7_dias': favoritos_7_dias,
                'top_filmes': list(filmes_favoritos),
            },
            'watchlist': {
                'total': total_watchlist,
                'assistidos': assistidos,
                'pendentes': total_watchlist - assistidos,
                'top_filmes': list(filmes_comentados),
            },
        })
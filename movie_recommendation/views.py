import os
import anthropic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from favorites.models import Favorito
from watchlist.models import Watchlist
from comments.models import Comentario


class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # busca dados do usuário
        favoritos = Favorito.objects.filter(usuario=user).values('titulo')
        watchlist = Watchlist.objects.filter(usuario=user).values('titulo', 'assistido')
        comentarios = Comentario.objects.filter(usuario=user).values('titulo', 'nota', 'texto')

        # montas listas para API da IA
        filmes_favoritos = [f['titulo'] for f in favoritos]
        filmes_watchlist = [w['titulo'] for w in watchlist]
        filmes_assistidos = [w['titulo'] for w in watchlist if w['assistido']]

        notas = {c['titulo']: c['nota'] for c in comentarios if c['nota']}
        comentarios_texto = [
            f"- {c['titulo']} (nota {c['nota']}/10): {c['texto']}"
            for c in comentarios
            if c['nota'] or c['texto']
        ]

        if not filmes_favoritos and not filmes_assistidos and not notas:
            return Response({
                'recommendations': [],
                'message': 'Adicione filmes aos favoritos ou watchlist para receber recomendações personalizadas!'
            })

        prompt_parts = [f"Usuário: {user.nome}\n"]

        if filmes_favoritos:
            prompt_parts.append(f"Filmes favoritos: {', '.join(filmes_favoritos)}")

        if filmes_assistidos:
            prompt_parts.append(f"Filmes assistidos na watchlist: {', '.join(filmes_assistidos)}")

        if filmes_watchlist:
            nao_assistidos = [w['titulo'] for w in watchlist if not w['assistido']]
            if nao_assistidos:
                prompt_parts.append(f"Quer assistir (watchlist): {', '.join(nao_assistidos)}")

        if comentarios_texto:
            prompt_parts.append("Avaliações feitas pelo usuário:\n" + "\n".join(comentarios_texto))

        perfil_usuario = "\n".join(prompt_parts)

        prompt = f"""Com base no perfil de gosto cinematográfico do usuário abaixo, recomende exatamente 6 filmes que ele provavelmente vai adorar mas que NÃO estão na lista de favoritos ou watchlist dele.

{perfil_usuario}

Responda APENAS em JSON válido, sem texto adicional, no seguinte formato:
{{
  "recommendations": [
    {{
      "titulo": "Nome do Filme",
      "ano": 2023,
      "genero": "Ação, Aventura",
      "motivo": "Curta explicação de 1-2 frases de por que esse filme combina com o gosto do usuário",
      "tmdb_query": "Nome do Filme ano"
    }}
  ]
}}"""

        # API da Anthropic
        try:
            client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
            message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            import json
            content = message.content[0].text.strip()
            data = json.loads(content)

            return Response({
                'recommendations': data.get('recommendations', []),
                'message': None
            })

        except json.JSONDecodeError:
            return Response({'error': 'Erro ao processar resposta da IA'}, status=500)
        except Exception as e:
            return Response({'error': f'Erro ao gerar recomendações: {str(e)}'}, status=500)
import json
import google.generativeai as genai
from django.conf import settings
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

        # monta listas para o prompt
        filmes_favoritos = [f['titulo'] for f in favoritos]
        filmes_assistidos = [w['titulo'] for w in watchlist if w['assistido']]

        notas = {c['titulo']: c['nota'] for c in comentarios if c['nota']}
        comentarios_texto = [
            f"- {c['titulo']} (nota {c['nota']}/10): {c['texto']}"
            for c in comentarios
            if c['nota'] or c['texto']
        ]

        # se o usuário não tem dados suficientes, retorna aviso
        if not filmes_favoritos and not filmes_assistidos and not notas:
            return Response({
                'recommendations': [],
                'message': 'Adicione filmes aos favoritos ou watchlist para receber recomendações personalizadas!'
            })

        # prompt para API da IA
        prompt_parts = [f"Usuário: {user.nome}\n"]

        if filmes_favoritos:
            prompt_parts.append(f"Filmes favoritos: {', '.join(filmes_favoritos)}")

        if filmes_assistidos:
            prompt_parts.append(f"Filmes assistidos na watchlist: {', '.join(filmes_assistidos)}")

        nao_assistidos = [w['titulo'] for w in watchlist if not w['assistido']]
        if nao_assistidos:
            prompt_parts.append(f"Quer assistir (watchlist): {', '.join(nao_assistidos)}")

        if comentarios_texto:
            prompt_parts.append("Avaliações feitas pelo usuário:\n" + "\n".join(comentarios_texto))

        perfil_usuario = "\n".join(prompt_parts)

        prompt = f"""Com base no perfil de gosto cinematográfico do usuário abaixo, recomende exatamente 10 filmes que ele provavelmente vai adorar mas que NÃO estão na lista de favoritos ou watchlist dele.

{perfil_usuario}

Responda APENAS em JSON válido, sem texto adicional, sem blocos de código, no seguinte formato:
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

        # API do Gemini
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)

            content = response.text.strip()

            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            data = json.loads(content)

            return Response({
                'recommendations': data.get('recommendations', []),
                'message': None
            })

        except json.JSONDecodeError:
            return Response({'error': 'Erro ao processar resposta da IA'}, status=500)
        except Exception as e:
            return Response({'error': f'Erro ao gerar recomendações: {str(e)}'}, status=500)
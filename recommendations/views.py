import json
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from django.conf import settings
from django.core.cache import cache

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

        # força nova geração de recomendações quando clicar no botão
        force = request.GET.get("force") == "true"

        cache_key = f"recommendations_{user.id}"

        # usa cache
        if not force:
            cached = cache.get(cache_key)
            if cached:
                return Response(cached)

        favoritos = Favorito.objects.filter(usuario=user).values('titulo')

        watchlist = Watchlist.objects.filter(usuario=user).values('titulo', 'assistido')

        comentarios = Comentario.objects.filter(usuario=user).values('titulo', 'nota', 'texto')

        filmes_favoritos = [f['titulo'] for f in favoritos]

        filmes_assistidos = [w['titulo'] for w in watchlist if w['assistido']]

        notas = {c['titulo']: c['nota'] for c in comentarios if c['nota']}

        comentarios_texto = [f"- {c['titulo']} (nota {c['nota']}/10): {c['texto']}"
            for c in comentarios
            if c['nota'] or c['texto']
        ]

        if not filmes_favoritos and not filmes_assistidos and not notas:
            return Response({
                "recommendations": [],
                "message": (
                    "Adicione filmes aos favoritos ou watchlist "
                    "para receber recomendações personalizadas!"
                )
            })

        prompt_parts = [f"Usuário: {user.nome}\n"]

        if filmes_favoritos:
            prompt_parts.append(f"Filmes favoritos: {', '.join(filmes_favoritos)}")

        if filmes_assistidos:
            prompt_parts.append(f"Filmes assistidos: {', '.join(filmes_assistidos)}")

        nao_assistidos = [
            w['titulo']
            for w in watchlist
            if not w['assistido']
        ]

        if nao_assistidos:
            prompt_parts.append(f"Quer assistir: {', '.join(nao_assistidos)}")

        if comentarios_texto:
            prompt_parts.append("Avaliações feitas:\n" +"\n".join(comentarios_texto))

        perfil_usuario = "\n".join(prompt_parts)

        prompt = f"""
Com base no perfil abaixo, recomende exatamente 5 filmes.

NÃO repita filmes já presentes nos favoritos
ou watchlist do usuário.

{perfil_usuario}

Responda SOMENTE em JSON válido:

{{
  "recommendations": [
    {{
      "titulo": "Nome do Filme",
      "ano": 2023,
      "genero": "Ação, Aventura",
      "motivo": "Explicação curta",
      "tmdb_query": "Nome do Filme 2023"
    }}
  ]
}}
"""

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)

            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(prompt)

            content = response.text.strip()

            if content.startswith("```"):
                content = (
                    content
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            data = json.loads(content)

            result = {
                "recommendations": data.get(
                    "recommendations",
                    []
                ),
                "message": None
            }

            # cache por 30 minutos
            cache.set(cache_key,result,timeout=60 * 30)

            return Response(result)
        
        except ResourceExhausted:

            cached = cache.get(cache_key)

            if cached:
                return Response(cached)

            return Response(
                {
                    "recommendations": [],
                    "message":
                        "O limite diário de recomendações foi atingido. "
                        "Tente novamente amanhã."
                },
                status=429
            )


        except json.JSONDecodeError:
            return Response({"error":"Erro ao processar resposta da IA"},status=500)

        except Exception as e:
            return Response({"error":f"Erro ao gerar recomendações: {str(e)}"},status=500)
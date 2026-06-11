<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient } from '../utils/axiosConfig'
import axios from 'axios'

const router = useRouter()
const recommendations = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const message = ref('')
const posters = ref<Record<number, string>>({})

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY

const fetchRecommendations = async () => {
  loading.value = true
  error.value = ''
  message.value = ''
  recommendations.value = []

  try {
    const { data } = await apiClient.get('/recomendacoes/')

    if (data.message) {
      message.value = data.message
    }

    recommendations.value = data.recommendations || []

    // Busca poster de cada filme no TMDB
    for (let i = 0; i < recommendations.value.length; i++) {
      const rec = recommendations.value[i]
      try {
        const tmdb = await axios.get(
          `https://api.themoviedb.org/3/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(rec.tmdb_query)}&language=pt-BR`
        )

        console.log(rec.tmdb_query)
        console.log(tmdb.data.results)
        
        const result = tmdb.data.results?.[0]
        if (result?.poster_path) {
          posters.value[i] = result.poster_path
          recommendations.value[i].tmdb_id = result.id
        }
      } catch {
        // Sem poster, tudo bem
      }
    }
  } catch (err: any) {
    if (err.response?.status === 401) {
      router.push('/login')
    } else {
      error.value = err.response?.data?.error || 'Erro ao buscar recomendações'
    }
  } finally {
    loading.value = false
  }
}

onMounted(fetchRecommendations)
</script>

<template>
  <div style="width: 100%; max-width: 1600px; margin: 0 auto; padding: 0 40px;">

    <!-- TÍTULO -->
    <div style="margin-bottom: 40px;">
      <h1 style="
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #7B2FF7, #00C6FF);
        -webkit-background-clip: text;
        color: transparent;
      ">
        🤖 Recomendações para Você
      </h1>
      <p style="color: #aaa;">
        Seleção de filmes com base nos seus favoritos, watchlist e avaliações
      </p>
    </div>

    <!-- ERRO -->
    <div v-if="error" style="
      background: linear-gradient(135deg, #3e0f2b, #4b1575);
      border-left: 4px solid #ff3cac;
      color: #ffccdd;
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 30px;
    ">
      ⚠️ {{ error }}
    </div>

    <!-- LOADING -->
    <div v-if="loading" style="text-align: center; padding: 80px;">
      <div style="
        width: 60px; height: 60px;
        border: 4px solid #222;
        border-top-color: #7B2FF7;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto;
      "></div>
      <p style="margin-top: 20px; color: #888; font-size: 16px;">
        🧠 Analisando seu gosto cinematográfico...
      </p>
    </div>

    <!-- SEM DADOS -->
    <div v-else-if="message" style="text-align: center; padding: 80px 20px;">
      <div style="font-size: 64px; margin-bottom: 20px;">🎬</div>
      <h2 style="
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #FF3CAC, #7B2FF7);
        -webkit-background-clip: text;
        color: transparent;
      ">
        Ainda sem dados suficientes sobre seu perfil
      </h2>
      <p style="color: #aaa; margin-bottom: 30px; max-width: 450px; margin: 0 auto 30px;">
        {{ message }}
      </p>
      <button
        @click="router.push('/')"
        style="
          background: linear-gradient(135deg, #7B2FF7, #00C6FF);
          color: white;
          padding: 14px 28px;
          border: none;
          border-radius: 999px;
          font-weight: bold;
          cursor: pointer;
          font-size: 15px;
        "
      >
        🎬 Explorar Filmes
      </button>
    </div>

    <!-- RECOMENDAÇÕES -->
    <div v-else-if="recommendations.length > 0">
      <p style="color: #888; margin-bottom: 30px;">
        {{ recommendations.length }} recomendações personalizadas
      </p>

      <div style="
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 28px;
      ">
        <div
          v-for="(rec, index) in recommendations"
          :key="index"
          style="
            background: #1A1A2E;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: all 0.3s;
            cursor: pointer;
            border: 1px solid rgba(123,47,247,0.2);
          "
          @mouseenter="($event.currentTarget as HTMLElement).style.transform = 'scale(1.03)'; ($event.currentTarget as HTMLElement).style.boxShadow = '0 0 30px rgba(123,47,247,0.5)'"
          @mouseleave="($event.currentTarget as HTMLElement).style.transform = 'scale(1)'; ($event.currentTarget as HTMLElement).style.boxShadow = '0 10px 30px rgba(0,0,0,0.5)'"
          @click="rec.tmdb_id && router.push(`/movie/${rec.tmdb_id}`)"
        >
          <!-- POSTER -->
          <div style="position: relative; height: 340px; background: #0f0f1b; overflow: hidden;">
            <img
              v-if="posters[index]"
              :src="`https://image.tmdb.org/t/p/w400${posters[index]}`"
              :alt="rec.titulo"
              style="width: 100%; height: 100%; object-fit: cover;"
            />
            <!-- Placeholder sem poster -->
            <div v-else style="
              width: 100%; height: 100%;
              display: flex; flex-direction: column;
              align-items: center; justify-content: center;
              background: linear-gradient(135deg, #1a1a2e, #16213e);
            ">
              <span style="font-size: 48px;">🎬</span>
              <span style="color: #555; font-size: 13px; margin-top: 8px;">Sem poster</span>
            </div>

            <!-- Badge IA -->
            <div style="
              position: absolute; top: 10px; left: 10px;
              background: linear-gradient(135deg, #7B2FF7, #00C6FF);
              color: white; padding: 4px 10px;
              border-radius: 999px; font-size: 11px;
              font-weight: bold; letter-spacing: 0.5px;
            ">
              Você pode gostar
            </div>

            <!-- Badge gênero -->
            <div style="
              position: absolute; bottom: 10px; left: 10px; right: 10px;
              background: rgba(0,0,0,0.7);
              color: #aaa; padding: 4px 10px;
              border-radius: 8px; font-size: 12px;
              backdrop-filter: blur(4px);
            ">
              {{ rec.genero }}
            </div>
          </div>

          <!-- INFO -->
          <div style="padding: 16px;">
            <h3 style="color: white; font-size: 16px; font-weight: bold; margin-bottom: 4px;">
              {{ rec.titulo }}
            </h3>
            <p style="color: #666; font-size: 13px; margin-bottom: 12px;">
              {{ rec.ano }}
            </p>

            <!-- Motivo da recomendação -->
            <div style="
              background: rgba(123,47,247,0.1);
              border-left: 3px solid #7B2FF7;
              border-radius: 0 8px 8px 0;
              padding: 10px 12px;
              margin-bottom: 14px;
            ">
              <p style="color: #ccc; font-size: 13px; line-height: 1.5; margin: 0;">
                💡 {{ rec.motivo }}
              </p>
            </div>

            <button
              v-if="rec.tmdb_id"
              @click.stop="router.push(`/movie/${rec.tmdb_id}`)"
              style="
                background: linear-gradient(135deg, #7B2FF7, #00C6FF);
                border: none; color: white;
                padding: 9px 14px; border-radius: 8px;
                font-weight: bold; cursor: pointer;
                font-size: 13px; width: 100%;
              "
            >
              🎥 Ver detalhes
            </button>
          </div>
        </div>
      </div>

      <!-- BOTÃO NOVAS RECOMENDAÇÕES -->
      <div style="text-align: center; margin-top: 50px;">
        <button
          @click="fetchRecommendations"
          :disabled="loading"
          style="
            background: linear-gradient(135deg, #FF3CAC, #7B2FF7);
            color: white; border: none;
            padding: 14px 36px; border-radius: 999px;
            font-weight: bold; cursor: pointer;
            font-size: 16px;
            box-shadow: 0 0 20px rgba(255,60,172,0.4);
          "
        >
          🔄 Gerar novas recomendações
        </button>
      </div>
    </div>

  </div>
</template>

<style>
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
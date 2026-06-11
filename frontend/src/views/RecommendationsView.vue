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

const fetchPosters = async () => {
  const promises = recommendations.value.map(async (rec, index) => {
    try {
      const tmdb = await axios.get(
        'https://api.themoviedb.org/3/search/movie',
        {
          params: {
            api_key: TMDB_API_KEY,
            query: rec.titulo,
            language: 'pt-BR'
          }
        }
      )

      const result = tmdb.data.results?.[0]

      if (result?.poster_path) {
        posters.value[rec.titulo] = result.poster_path
        recommendations.value[index].tmdb_id = result.id
      }
    } catch {
      console.error('Erro ao buscar poster:', rec.tmdb_query, err)
    }
    console.log('Busca:', rec.tmdb_query)
    console.log('Resultado TMDB:', tmdb.data.results?.[0])
  })

  await Promise.all(promises)
}

const fetchRecommendations = async (force = false) => {
  loading.value = true
  error.value = ''
  message.value = ''

  try {
    const { data } = await apiClient.get(
      `/recomendacoes/?force=${force}`
    )

    error.value = ''

    if (data.message) {
      message.value = data.message
    }

    recommendations.value = data.recommendations || []

    posters.value = {}

    await fetchPosters()

  } catch (err: any) {

    if (err.response?.status === 429) {
      message.value =
        'Limite diário de recomendações foi atingido. Tente novamente amanhã.'
      return
    }

    if (err.response?.status === 401) {
      return
    }

    error.value = ''

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
        Seleção personalizada baseada no seu histórico
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
        width: 60px;
        height: 60px;
        border: 4px solid #222;
        border-top-color: #7B2FF7;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto;
      "></div>

      <p style="margin-top: 20px; color: #888;">
        🧠 Gerando recomendações...
      </p>
    </div>

    <!-- SEM DADOS -->
    <div v-else-if="message" style="text-align: center; padding: 80px 20px;">
      <div style="font-size: 64px;">🎬</div>

      <h2 style="color: white; margin-top: 20px;">
        Ainda sem dados suficientes
      </h2>

      <p style="color: #aaa; max-width: 500px; margin: 20px auto;">
        {{ message }}
      </p>

      <button
        @click="router.push('/')"
        style="
          background: linear-gradient(135deg, #7B2FF7, #00C6FF);
          color: white;
          padding: 14px 28px;
          border-radius: 999px;
          border: none;
          cursor: pointer;
          font-weight: bold;
        "
      >
        🎬 Explorar filmes
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
            cursor: pointer;
            border: 1px solid rgba(123,47,247,0.2);
            transition: 0.3s;
          "
          @mouseenter="($event.currentTarget as HTMLElement).style.transform = 'scale(1.03)'"
          @mouseleave="($event.currentTarget as HTMLElement).style.transform = 'scale(1)'"
          @click="rec.tmdb_id && router.push(`/movie/${rec.tmdb_id}`)"
        >

          <!-- POSTER -->
          <div style="height: 340px; background: #0f0f1b;">

            <img
              v-if="posters[rec.titulo]"
              :src="`https://image.tmdb.org/t/p/w400${posters[rec.titulo]}`"
              style="width: 100%; height: 100%; object-fit: cover;"
            />

            <div v-else style="
              width: 100%;
              height: 100%;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              color: #555;
            ">
              🎬<br>
              Sem poster
            </div>

          </div>

          <!-- INFO -->
          <div style="padding: 16px;">
            <h3 style="color: white; font-size: 16px;">
              {{ rec.titulo }}
            </h3>

            <p style="color: #666; font-size: 13px;">
              {{ rec.ano }}
            </p>

            <p style="
              color: #ccc;
              font-size: 13px;
              margin-top: 10px;
              line-height: 1.4;
            ">
              💡 {{ rec.motivo }}
            </p>

          </div>

        </div>

      </div>

      <!-- BOTÃO NOVAS RECOMENDAÇÕES -->
      <div style="text-align: center; margin-top: 50px;">
        <button
          @click="fetchRecommendations(true)"
          :disabled="loading"
          style="
            background: linear-gradient(135deg, #FF3CAC, #7B2FF7);
            color: white;
            padding: 14px 36px;
            border-radius: 999px;
            border: none;
            cursor: pointer;
            font-weight: bold;
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
  to {
    transform: rotate(360deg);
  }
}
</style>
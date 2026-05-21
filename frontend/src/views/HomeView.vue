<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { BACKEND_URL } from '../utils/api'

const movies = ref<any[]>([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  await fetchPopularMovies()
})

const fetchPopularMovies = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.get(`${BACKEND_URL}/filmes/populares/`)
    movies.value = response.data.results
  } catch (err) {
    error.value = 'Erro ao carregar filmes: ' + (err as any).message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto px-4" style="max-width:1600px">

    <!-- Título -->
    <section class="mb-5">
      <h1 class="fw-black mb-2 mf-gradient-text" style="font-size:clamp(32px,5vw,48px);letter-spacing:0.06em">
        🎬 Filmes Populares
      </h1>
      <p style="color:rgba(229,231,235,0.82)">As escolhas mais quentes do momento — direto do mundo do streaming.</p>
    </section>

    <!-- Erro -->
    <div v-if="error" class="alert mb-4 p-3" style="background:linear-gradient(135deg,#3e0f2b,#4b1575);border-left:4px solid #ff3cac;color:#ffccdd;border-radius:12px">
      ⚠️ {{ error }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="mf-spinner"></div>
      <p class="mt-3" style="color:rgba(229,231,235,0.8)">Carregando filmes épicos...</p>
    </div>

    <!-- Vazio -->
    <div v-else-if="movies.length === 0" class="text-center py-5">
      <p class="fs-5" style="color:rgba(229,231,235,0.8)">📽️ Nenhum filme encontrado</p>
    </div>

    <!-- Grid de filmes -->
    <div v-else class="row row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-xl-6 g-4">
      <div v-for="movie in movies" :key="movie.id" class="col">
        <div class="mf-card h-100">
          <div class="position-relative" style="height:330px;overflow:hidden">
            <img
              v-if="movie.poster_path"
              :src="`https://image.tmdb.org/t/p/w400${movie.poster_path}`"
              :alt="movie.title"
              class="w-100 h-100 object-fit-cover"
              style="transition:transform 0.4s ease"
            />
            <div class="position-absolute inset-0" style="background:linear-gradient(180deg,rgba(15,15,27,0.1),rgba(15,15,27,0.8))"></div>
            <span class="position-absolute top-0 end-0 m-2 badge rounded-pill fw-bold" style="background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;font-size:13px">
              ⭐ {{ movie.vote_average?.toFixed(1) }}
            </span>
          </div>
          <div class="p-3">
            <h3 class="fw-bold mb-1" style="font-size:15px;color:#f8f8ff;line-height:1.3">{{ movie.title }}</h3>
            <p class="mb-1" style="font-size:13px;color:#9ca3af">{{ movie.release_date?.split('-')[0] || 'Data não informada' }}</p>
            <p class="mb-2" style="font-size:13px;color:#adb5bd;line-height:1.4;height:38px;overflow:hidden">{{ movie.overview || 'Sem sinopse' }}</p>
            <router-link :to="`/movie/${movie.id}`" class="fw-bold" style="color:#00C6FF;font-size:13px">Detalhes →</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

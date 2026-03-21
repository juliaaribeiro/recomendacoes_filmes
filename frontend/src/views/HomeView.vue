<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { setTargetStyle } from '../composables/useHoverStyle'
import { BACKEND_URL } from '../utils/api'

const movies = ref<any[]>([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  console.log('HomeView mounted')
  await fetchPopularMovies()
})

const fetchPopularMovies = async () => {
  loading.value = true
  error.value = ''
  try {
    console.log('Fetching movies from:', `${BACKEND_URL}/filmes/populares/`)
    const response = await axios.get(`${BACKEND_URL}/filmes/populares/`)
    console.log('Movies fetched:', response.data.results.length)
    movies.value = response.data.results
  } catch (err) {
    error.value = 'Erro ao carregar filmes: ' + (err as any).message
    console.error('Error fetching movies:', err)
  } finally {
    loading.value = false
  }
}

const setMovieImageHover = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, { transform: hover ? 'scale(1.08)' : 'scale(1)' })
}
</script>

<template>
  <div style="width: 100%; max-width: 1600px; margin: 0 auto; padding: 0 40px;">
    <section style="margin-bottom: 40px;">
      <h1 style="font-size: 48px; font-weight: 900; margin-bottom: 10px; background: linear-gradient(135deg, #FF3CAC 0%, #00C6FF 100%); -webkit-background-clip: text; color: transparent; text-shadow: 0 0 20px rgba(123, 47, 247, 0.5); letter-spacing: 0.06em;">🎬 Filmes Populares</h1>
      <p style="font-size: 16px; color: rgba(229,231,235,0.82); margin: 0;">As escolhas mais quentes do momento — direto do mundo do streaming.</p>
    </section>

    <section style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center;">
      <span style="font-size: 14px; color: rgba(229,231,235,0.76);">Deslize no carrossel para navegar</span>
      <span style="font-size: 13px; color: rgba(229,231,235,0.6);">Visual moderno com parallax</span>
    </section>

    <div v-if="error" style="background: linear-gradient(135deg, #3e0f2b 0%, #4b1575 100%); border-left: 4px solid #ff3cac; color: #ffccdd; padding: 16px; margin-bottom: 30px; border-radius: 12px; font-weight: 500;">
      ⚠️ {{ error }}
    </div>

    <div v-if="loading" style="text-align: center; padding: 80px 0;">
      <div style="display: inline-block; width: 50px; height: 50px; border: 4px solid rgba(255,255,255,0.2); border-top-color: #00C6FF; border-radius: 50%; animation: spin 1s linear infinite;"></div>
      <p style="margin-top: 20px; color: rgba(229,231,235,0.8); font-size: 16px;">Carregando filmes épicos...</p>
    </div>

    <div v-else-if="movies.length === 0" style="text-align: center; padding: 80px 0;">
      <p style="font-size: 18px; color: rgba(229,231,235,0.8);">📽️ Nenhum filme encontrado</p>
    </div>

    <div v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 26px;">
      <div v-for="movie in movies" :key="movie.id" style="position: relative; border-radius: 20px; overflow: hidden; background: #1A1A2E; box-shadow: 0 8px 40px rgba(0,0,0,0.5); transform: translateY(0); transition: transform 0.3s ease, box-shadow 0.3s ease; cursor: pointer;">
        <div style="position: relative; height: 330px; overflow: hidden;">
          <img
            v-if="movie.poster_path"
            :src="`https://image.tmdb.org/t/p/w400${movie.poster_path}`"
            :alt="movie.title"
            style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease;"
            @mouseenter="setMovieImageHover($event, true)"
            @mouseleave="setMovieImageHover($event, false)"
          />
          <div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(15, 15, 27, 0.1), rgba(15, 15, 27, 0.8));"></div>
          <div style="position: absolute; top: 16px; right: 16px; background: linear-gradient(135deg, #FFD700, #FF8C00); color: #000; padding: 6px 12px; border-radius: 999px; font-weight: 700; font-size: 13px; box-shadow: 0 0 12px rgba(255, 140, 0, 0.45);">
            ⭐ {{ movie.vote_average?.toFixed(1) }}
          </div>
          <div style="position: absolute; inset: 0; opacity: 0; transition: opacity 0.25s ease; background: rgba(11, 17, 47, 0.56); display: flex; justify-content: center; align-items: center; gap: 10px;">
            <router-link :to="`/movie/${movie.id}`" style="padding: 10px 14px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.45); color: #fff; font-weight: 700; background: rgba(27, 27, 52, 0.8);">▶ Assistir</router-link>
            <button style="padding: 10px 14px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.45); color: #fff; font-weight: 700; background: rgba(123,47,247,0.85);">❤️ Favoritar</button>
          </div>
        </div>
        <div style="padding: 18px;">
          <h3 style="font-size: 16px; font-weight: 800; color: #f8f8ff; margin-bottom: 6px; line-height: 1.3;">{{ movie.title }}</h3>
          <p style="font-size: 13px; color: #9ca3af; margin-bottom: 8px;">{{ movie.release_date?.split('-')[0] || 'Data não informada' }}</p>
          <p style="font-size: 13px; color: #adb5bd; margin-bottom: 10px; line-height: 1.4; height: 38px; overflow: hidden; text-overflow: ellipsis;">{{ movie.overview || 'Sem sinopse' }}</p>
          <router-link :to="`/movie/${movie.id}`" style="display: inline-block; color: #00C6FF; font-weight: 700; text-decoration: none;">Detalhes →</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@keyframes spin { to { transform: rotate(360deg); } }

div[style*="position: relative; border-radius: 20px; overflow: hidden"]:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 50px rgba(88, 50, 255, 0.55);
}

div[style*="position: relative; inset: 0; opacity: 0;"] {
  display: flex;
}

div[style*="position: relative; inset: 0; background: rgba(11, 17, 47, 0.56)"]:hover {
  opacity: 1 !important;
}
</style>

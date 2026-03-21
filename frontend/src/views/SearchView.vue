<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'
import { TMDB_API_KEY, TMDB_BASE_URL } from '../utils/api'

const query = ref('')
const movies = ref<any[]>([])
const loading = ref(false)
const searched = ref(false)

const getTarget = (event: Event) => {
  const target = event.target as HTMLElement | null
  return target
}

const handleInputFocus = (event: FocusEvent) => {
  const target = getTarget(event)
  if (target) {
    target.style.borderColor = '#667eea'
    target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)'
  }
}

const handleInputBlur = (event: FocusEvent) => {
  const target = getTarget(event)
  if (target) {
    target.style.borderColor = '#e5e7eb'
    target.style.boxShadow = 'none'
  }
}

const handleBtnHover = (event: MouseEvent, hover: boolean) => {
  const target = event.target as HTMLElement | null
  if (target) {
    target.style.opacity = hover ? '0.9' : '1'
    target.style.transform = hover ? 'translateY(-2px)' : 'translateY(0)'
  }
}

const handleCardHover = (event: MouseEvent, hover: boolean) => {
  const target = event.currentTarget as HTMLElement | null
  if (target) {
    target.style.transform = hover ? 'translateY(-8px)' : 'translateY(0)'
    target.style.boxShadow = hover ? '0 12px 30px rgba(102,126,234,0.2)' : '0 4px 15px rgba(0,0,0,0.08)'
  }
}

const handleImageHover = (event: MouseEvent, hover: boolean) => {
  const target = event.target as HTMLImageElement | null
  if (target) {
    target.style.transform = hover ? 'scale(1.05)' : 'scale(1)'
  }
}

const handleSearch = async () => {
  if (!query.value.trim()) {
    return
  }

  loading.value = true
  searched.value = true

  try {
    const response = await axios.get(
      `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${query.value}&language=pt-BR`
    )
    movies.value = response.data.results
  } catch (error) {
    console.error('Erro ao buscar filmes:', error)
    movies.value = []
  } finally {
    loading.value = false
  }
}

const handleKeyup = (e: KeyboardEvent) => {
  if (e.key === 'Enter') {
    handleSearch()
  }
}
</script>

<template>
  <div style="width: 100%; max-width: 1600px; margin: 0 auto; padding: 0 40px;">
    <div style="margin-bottom: 40px;">
      <h1 style="font-size: 42px; font-weight: bold; margin-bottom: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🔍 Buscar Filmes</h1>
      <p style="font-size: 16px; color: #666; margin: 0;">Digite o nome do filme que você deseja encontrar</p>
    </div>
    
    <div style="display: flex; gap: 12px; margin-bottom: 40px;">
      <input
        v-model="query"
        type="text"
        placeholder="Digite o nome do filme..."
        @keyup="handleKeyup"
        style="flex: 1; padding: 14px 18px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 15px; transition: border-color 0.3s, box-shadow 0.3s;"
        @focus="handleInputFocus"
        @blur="handleInputBlur"
      />
      <button
        @click="handleSearch"
        :disabled="loading"
        style="padding: 14px 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 15px; transition: opacity 0.3s, transform 0.2s; white-space: nowrap;"
        @mouseenter="handleBtnHover($event, true)"
        @mouseleave="handleBtnHover($event, false)"
      >
        {{ loading ? 'Buscando...' : 'Buscar' }}
      </button>
    </div>

    <div v-if="loading" style="text-align: center; padding: 80px 40px;">
      <div style="display: inline-block; width: 50px; height: 50px; border: 4px solid #e5e7eb; border-top-color: #667eea; border-radius: 50%; animation: spin 1s linear infinite;"></div>
      <p style="margin-top: 20px; color: #666; font-size: 16px;">Buscando filmes...</p>
    </div>

    <div v-else-if="searched && movies.length === 0" style="text-align: center; padding: 80px 40px;">
      <p style="font-size: 18px; color: #666;">Nenhum filme encontrado para "{{ query }}"</p>
    </div>

    <div v-else-if="searched && movies.length > 0">
      <p style="color: #666; margin-bottom: 30px; font-weight: 500; font-size: 15px;">{{ movies.length }} filme(s) encontrado(s)</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 28px;">
          <div v-for="movie in movies" :key="movie.id" style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: all 0.3s ease; cursor: pointer;" @mouseenter="handleCardHover($event, true)" @mouseleave="handleCardHover($event, false)">
          <div style="position: relative; overflow: hidden; height: 330px; background-color: #e5e7eb;">
            <img 
              v-if="movie.poster_path"
              :src="`https://image.tmdb.org/t/p/w300${movie.poster_path}`" 
              :alt="movie.title"
              style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;"
              @mouseenter="handleImageHover($event, true)"
              @mouseleave="handleImageHover($event, false)"
            />
            <div style="position: absolute; top: 12px; right: 12px; background-color: rgba(102, 126, 234, 0.95); color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 13px;">⭐ {{ movie.vote_average?.toFixed(1) }}</div>
          </div>
          <div style="padding: 16px;">
            <h3 style="font-weight: bold; font-size: 15px; margin-bottom: 8px; line-height: 1.4; color: #1a202c;">{{ movie.title }}</h3>
            <p style="color: #718096; font-size: 13px; margin-bottom: 12px;">{{ movie.release_date?.split('-')[0] || 'Data não informada' }}</p>
            <router-link :to="`/movie/${movie.id}`" style="display: inline-block; color: #667eea; text-decoration: none; font-weight: 600; font-size: 13px; transition: color 0.3s;" @mouseenter="(e) => (e.target as HTMLElement).style.color = '#764ba2'" @mouseleave="(e) => (e.target as HTMLElement).style.color = '#667eea'">Ver detalhes →</router-link>
          </div>
        </div>
      </div>
    </div>

    <div v-else style="text-align: center; padding: 80px 40px;">
      <p style="color: #666; font-size: 16px;">Digite o nome de um filme para começar a busca</p>
    </div>
  </div>
</template>

<style>
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
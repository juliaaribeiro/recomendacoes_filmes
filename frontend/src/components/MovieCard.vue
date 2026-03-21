<template>
  <router-link :to="`/movie/${movie.id}`" class="block">
    <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl hover:scale-105 transition duration-200">
      <div class="relative overflow-hidden bg-gray-200 h-64">
        <img
          v-if="movie.poster_path"
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          :alt="movie.title"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
          Sem imagem
        </div>
      </div>
      <div class="p-4">
        <h3 class="text-lg font-semibold truncate" :title="movie.title">{{ movie.title }}</h3>
        <p class="text-sm text-gray-600 mb-2">{{ movie.release_date?.split('-')[0] || 'N/A' }}</p>
        <div class="flex items-center justify-between">
          <span v-if="movie.vote_average" class="text-yellow-500 font-bold">
            ⭐ {{ (movie.vote_average / 2).toFixed(1) }}
          </span>
          <span v-else class="text-gray-400">N/A</span>
          <button @click.prevent="toggleFavorite" class="text-red-500 hover:text-red-700">
            {{ isFavorited ? '❤️' : '🤍' }}
          </button>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  movie: any
}>()

const isFavorited = ref(false)

const toggleFavorite = () => {
  isFavorited.value = !isFavorited.value
  // Aqui você poderia fazer uma requisição para salvar nos favoritos do usuário
}
</script>
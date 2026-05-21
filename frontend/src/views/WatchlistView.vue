<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient } from '../utils/axiosConfig'

const router = useRouter()
const watchlist = ref<any[]>([])
const loading = ref(false)

const fetchWatchlist = async () => {
  loading.value = true
  try {
    const { data } = await apiClient.get('/watchlist/')
    
    console.log('DADOS WATCHLIST:', data) 

    watchlist.value = data
  } catch (error) {
    console.error('Erro ao buscar watchlist:', error)
    watchlist.value = []
  } finally {
    loading.value = false
  }
}

const removeFromWatchlist = async (id: number) => {
  try {
    await apiClient.delete(`/watchlist/${id}/`)
    watchlist.value = watchlist.value.filter(w => w.id !== id)
  } catch (error) {
    alert('Erro ao remover da watchlist')
  }
}

const toggleWatched = async (movie: any) => {
  try {
    await apiClient.patch(`/watchlist/${movie.id}/`, {
      assistido: !movie.assistido,
    })
    watchlist.value = watchlist.value.map(w =>
      w.id === movie.id ? { ...w, assistido: !w.assistido } : w
    )
  } catch (error) {
    alert('Erro ao atualizar status de assistido')
  }
}

const adjustScale = (event: MouseEvent, hover: boolean) => {
  const target = event.target as HTMLElement | null
  if (target) {
    target.style.transform = hover ? 'scale(1.05)' : 'scale(1)'
  }
}

const adjustCardHover = (event: MouseEvent, hover: boolean) => {
  const target = event.currentTarget as HTMLElement | null
  if (target) {
    target.style.transform = hover ? 'scale(1.05)' : 'scale(1)'
    target.style.boxShadow = hover ? '0 0 25px #00C6FF' : '0 10px 30px rgba(0,0,0,0.5)'
  }
}

onMounted(fetchWatchlist)
</script>

<template>
  <div style="width: 100%; max-width: 1600px; margin: 0 auto; padding: 0 40px;">
    
    <!-- TÍTULO -->
    <div style="margin-bottom: 40px;">
      <h1 style="
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #00C6FF, #2563eb);
        -webkit-background-clip: text;
        color: transparent;
      ">
        📋 Minha Watchlist
      </h1>
      <p style="color: #aaa;">Filmes que você quer assistir depois</p>
    </div>

    <!-- LOADING -->
    <div v-if="loading" style="text-align: center; padding: 80px;">
      <div style="width: 50px; height: 50px; border: 4px solid #222; border-top-color: #00C6FF; border-radius: 50%; animation: spin 1s linear infinite;"></div>
      <p style="margin-top: 20px; color: #888;">Carregando sua watchlist...</p>
    </div>

    <!-- VAZIO -->
    <div v-else-if="watchlist.length === 0" style="text-align: center; padding: 100px 20px;">
      
      <h2 style="
        font-size: 26px;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #00C6FF, #2563eb);
        -webkit-background-clip: text;
        color: transparent;
      ">
        Sua watchlist está vazia 🎬
      </h2>

      <p style="color: #aaa; margin-bottom: 30px;">
        Adicione filmes para assistir depois e organize sua lista
      </p>

      <button 
        @click="router.push('/')"
        style="
          background: linear-gradient(135deg, #00C6FF, #2563eb);
          color: white;
          padding: 14px 28px;
          border: none;
          border-radius: 999px;
          font-weight: bold;
          cursor: pointer;
          box-shadow: 0 0 15px rgba(0,198,255,0.5);
          transition: 0.3s;
        "
        @mouseenter="adjustScale($event, true)"
        @mouseleave="adjustScale($event, false)"
      >
        🔍 Explorar Filmes
      </button>
    </div>

    <!-- LISTA -->
    <div v-else>
      <p style="color: #888; margin-bottom: 30px;">
        {{ watchlist.length }} filme(s) na sua lista
      </p>

      <div style="
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 28px;
      ">
        
        <div 
          v-for="movie in watchlist" 
          :key="movie.id"
          style="
            background: #1A1A2E;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: all 0.3s;
            cursor: pointer;
          "
          @mouseenter="adjustCardHover($event, true)"
          @mouseleave="adjustCardHover($event, false)"
        >

          <!-- POSTER -->
          <div style="position: relative;">
            <img 
              :src="`https://image.tmdb.org/t/p/w300${movie.poster}`"
              style="width: 100%; height: 330px; object-fit: cover;"
            />

            <!-- REMOVER -->
            <button 
              @click.stop="removeFromWatchlist(movie.id)"
              style="
                position: absolute;
                top: 10px;
                right: 10px;
                background: linear-gradient(135deg, #00C6FF, #2563eb);
                border: none;
                color: white;
                padding: 6px 10px;
                border-radius: 999px;
                cursor: pointer;
                font-size: 12px;
                box-shadow: 0 0 10px rgba(0,198,255,0.6);
              "
            >
              ❌
            </button>
          </div>

          <!-- INFO -->
          <div style="padding: 16px;">
            <h3 style="color: white; font-size: 15px; font-weight: bold; margin-bottom: 10px;">
              {{ movie.titulo }}
            </h3>

            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 12px;">
              <span
                :style="{
                  padding: '6px 10px',
                  borderRadius: '999px',
                  fontSize: '12px',
                  fontWeight: '700',
                  color: movie.assistido ? '#10b981' : '#fbbf24',
                  background: movie.assistido ? 'rgba(16,185,129,0.14)' : 'rgba(251,191,36,0.14)',
                }"
              >
                {{ movie.assistido ? 'Assistido' : 'Não assistido' }}
              </span>

              <button
                @click.stop="toggleWatched(movie)"
                style="
                  background: transparent;
                  border: 1px solid rgba(255,255,255,0.15);
                  color: white;
                  padding: 7px 12px;
                  border-radius: 999px;
                  cursor: pointer;
                  font-size: 12px;
                "
              >
                {{ movie.assistido ? 'Marcar como não assistido' : 'Marcar como assistido' }}
              </button>
            </div>

            <button
              @click="router.push(`/movie/${movie.filme_id}`)"
              style="
                background: linear-gradient(135deg, #00C6FF, #2563eb);
                border: none;
                color: white;
                padding: 8px 14px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                font-size: 13px;
                width: 100%;
              "
            >
              ▶ Ver detalhes
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style>
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
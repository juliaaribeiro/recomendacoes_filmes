<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { setCurrentTargetStyle, setTargetStyle } from '../composables/useHoverStyle'
import { apiClient } from '../utils/axiosConfig'

const router = useRouter()
const favorites = ref<any[]>([])
const loading = ref(false)

const fetchFavorites = async () => {
  loading.value = true
  try {
    const { data } = await apiClient.get('/favoritos/')
    
    console.log('DADOS FAVORITOS:', data)

    favorites.value = data
  } catch (error) {
    console.error('Erro ao buscar favoritos:', error)
    favorites.value = []
  } finally {
    loading.value = false
  }
}

const removeFavorite = async (id: number) => {
  try {
    await apiClient.delete(`/favoritos/${id}/`)
    favorites.value = favorites.value.filter(f => f.id !== id)
  } catch (error) {
    alert('Erro ao remover favorito')
  }
}

const adjustButtonOpacity = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, {
    opacity: hover ? '0.9' : '1',
    transform: hover ? 'translateY(-2px)' : 'translateY(0)'
  })
}

const adjustFavoriteCard = (event: MouseEvent, hover: boolean) => {
  setCurrentTargetStyle(event, {
    transform: hover ? 'scale(1.05)' : 'scale(1)',
    boxShadow: hover ? '0 0 25px #7B2FF7' : '0 10px 30px rgba(0,0,0,0.5)'
  })
}

onMounted(fetchFavorites)
</script>

<template>
  <div style="width: 100%; max-width: 1600px; margin: 0 auto; padding: 0 40px;">
    
    <!-- TÍTULO -->
    <div style="margin-bottom: 40px;">
      <h1 style="
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #FF3CAC, #00C6FF);
        -webkit-background-clip: text;
        color: transparent;
      ">
        ❤️ Meus Favoritos
      </h1>
      <p style="color: #aaa;">Seus filmes salvos para assistir depois</p>
    </div>

    <!-- LOADING -->
    <div v-if="loading" style="text-align: center; padding: 80px;">
      <div style="width: 50px; height: 50px; border: 4px solid #222; border-top-color: #7B2FF7; border-radius: 50%; animation: spin 1s linear infinite;"></div>
      <p style="margin-top: 20px; color: #888;">Carregando favoritos...</p>
    </div>

    <!-- SEM FAVORITOS -->
    <div v-else-if="favorites.length === 0" style="text-align: center; padding: 100px 20px;">
      
      <h2 style="
        font-size: 26px;
        margin-bottom: 16px;
      ">
        <span style="
          background: linear-gradient(135deg, #FF3CAC, #7B2FF7);
          -webkit-background-clip: text;
          color: transparent;
        ">
          Você ainda não tem favoritos
        </span>
        <span> 😢</span>
      </h2>

      <p style="color: #aaa; margin-bottom: 30px;">
        Explore filmes e adicione seus favoritos para vê-los aqui
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
          box-shadow: 0 0 15px rgba(123,47,247,0.5);
          transition: 0.3s;
        "
        @mouseenter="adjustButtonOpacity($event, true)"
        @mouseleave="adjustButtonOpacity($event, false)"
      >
        🎬 Ir para Home
      </button>
    </div>

    <!-- LISTA DE FAVORITOS -->
    <div v-else>
      <p style="color: #888; margin-bottom: 30px;">
        {{ favorites.length }} filme(s) favorito(s)
      </p>

      <div style="
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 28px;
      ">
        
        <div 
          v-for="movie in favorites" 
          :key="movie.id"
          style="
            background: #1A1A2E;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: all 0.3s;
            cursor: pointer;
          "
          @mouseenter="adjustFavoriteCard($event, true)"
          @mouseleave="adjustFavoriteCard($event, false)"
        >

          <!-- POSTER -->
          <div style="position: relative;">
            <img 
              :src="`https://image.tmdb.org/t/p/w300${movie.poster}`"
              style="width: 100%; height: 330px; object-fit: cover;"
            />

            <!-- BOTÃO REMOVER -->
            <button 
              @click.stop="removeFavorite(movie.id)"
              style="
                position: absolute;
                top: 10px;
                right: 10px;
                background: linear-gradient(135deg, #FF3CAC, #7B2FF7);
                border: none;
                color: white;
                padding: 6px 10px;
                border-radius: 999px;
                cursor: pointer;
                font-size: 12px;
                box-shadow: 0 0 10px rgba(255,60,172,0.6);
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

            <button
              @click="router.push(`/movie/${movie.filme_id}`)"
              style="
                background: linear-gradient(135deg, #00C6FF, #7B2FF7);
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
              🎥 Ver detalhes
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
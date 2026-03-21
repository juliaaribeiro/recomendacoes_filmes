<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { setTargetStyle } from '../composables/useHoverStyle'
import { TMDB_API_KEY, TMDB_BASE_URL } from '../utils/api'
import { apiClient } from '../utils/axiosConfig'

const route = useRoute()
const router = useRouter()
const { isLogged, user } = useAuth()

const movie = ref<any>(null)
const loading = ref(false)

// interação usuário
const isFavorite = ref(false)
const isInWatchlist = ref(false)

// avaliação + comentário
const rating = ref(0)
const comment = ref('')
const hoverRating = ref(0)
const submitting = ref(false)

const comments = ref<any[]>([])

const editingCommentId = ref<number | null>(null)
const editedCommentText = ref('')
const editedCommentRating = ref(0)

const setRating = (value: number) => {
  rating.value = value
}

// -----------------------------

onMounted(async () => {
  loading.value = true
  try {
    const movieId = route.params.id

    const response = await axios.get(
      `${TMDB_BASE_URL}/movie/${movieId}?api_key=${TMDB_API_KEY}&language=pt-BR`
    )

    movie.value = response.data

    await fetchComments()
    await checkFavorite()
    await checkWatchlist()

  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})

// -----------------------------
// 🔥 BUSCAR COMENTÁRIOS

const fetchComments = async () => {
  try {
    const { data } = await apiClient.get(`/comentarios/?filme=${route.params.id}`)
    // Handle both paginated and non-paginated responses
    comments.value = data.results ? data.results : (Array.isArray(data) ? data : [])
  } catch (err) {
    console.error(err)
    comments.value = []
  }
}

// -----------------------------
// 🔥 FAVORITOS / WATCHLIST

const checkFavorite = async () => {
  if (!isLogged.value) return
  try {
    const { data } = await apiClient.get(`/favoritos/?filme=${route.params.id}`)
    const favList = data.results ? data.results : (Array.isArray(data) ? data : [])
    isFavorite.value = favList.length > 0
  } catch {}
}

const checkWatchlist = async () => {
  if (!isLogged.value) return
  try {
    const { data } = await apiClient.get(`/watchlist/?filme=${route.params.id}`)
    const wlList = data.results ? data.results : (Array.isArray(data) ? data : [])
    isInWatchlist.value = wlList.length > 0
  } catch {}
}

// -----------------------------
// 🔥 TOGGLE

const toggleFavorite = async () => {
  if (!isLogged.value) {
    alert('Faça login para adicionar ou remover favoritos')
    router.push('/login')
    return
  }
  try {
    if (isFavorite.value) {
      const { data } = await apiClient.get(`/favoritos/?filme=${route.params.id}`)
      const favList = data.results ? data.results : (Array.isArray(data) ? data : [])
      const id = favList[0]?.id
      if (id) await apiClient.delete(`/favoritos/${id}/`)
    } else {
      await apiClient.post('/favoritos/', {
        filme_id: route.params.id,
        titulo: movie.value.title,
        poster: movie.value.poster_path || '',
      })
    }
    isFavorite.value = !isFavorite.value
  } catch (err: any) {
    const msg = err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao atualizar favorito'
    alert(msg)
  }
}

const toggleWatchlist = async () => {
  if (!isLogged.value) {
    alert('Faça login para adicionar ou remover da watchlist')
    router.push('/login')
    return
  }
  try {
    if (isInWatchlist.value) {
      const { data } = await apiClient.get(`/watchlist/?filme=${route.params.id}`)
      const wlList = data.results ? data.results : (Array.isArray(data) ? data : [])
      const id = wlList[0]?.id
      if (id) await apiClient.delete(`/watchlist/${id}/`)
    } else {
      await apiClient.post('/watchlist/', {
        filme_id: route.params.id,
        titulo: movie.value.title,
        poster: movie.value.poster_path || '',
      })
    }
    isInWatchlist.value = !isInWatchlist.value
  } catch (err: any) {
    const msg = err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao atualizar watchlist'
    alert(msg)
  }
}

// -----------------------------
// 🔥 ENVIOS

const submitComment = async () => {
  if (!rating.value || rating.value < 1 || rating.value > 10) {
    alert('Escolha uma nota de 1 a 10 antes de enviar')
    return
  }
  if (!comment.value.trim()) {
    alert('Digite um comentário')
    return
  }
  submitting.value = true
  try {
    const existingComment = comments.value.find((c: any) => c.usuario === user.value?.id)
    if (existingComment) {
      await apiClient.patch(`/comentarios/${existingComment.id}/`, {
        texto: comment.value,
        nota: rating.value,
      })
      alert('Comentário atualizado com sucesso!')
    } else {
      await apiClient.post('/comentarios/', {
        filme_id: route.params.id,
        texto: comment.value,
        titulo: movie.value.title,
        nota: rating.value,
      })
      alert('Comentário e nota enviados com sucesso!')
    }
    comment.value = ''
    rating.value = 0
    hoverRating.value = 0
    await fetchComments()
  } catch (err: any) {
    const msg = err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao registrar comentário'
    alert(msg)
  } finally {
    submitting.value = false
  }
}

const startEditComment = (comment: any) => {
  editingCommentId.value = comment.id
  editedCommentText.value = comment.texto
  editedCommentRating.value = comment.nota || 0
}

const cancelEditComment = () => {
  editingCommentId.value = null
  editedCommentText.value = ''
  editedCommentRating.value = 0
}

const updateComment = async (commentId: number) => {
  if (!editedCommentRating.value || editedCommentRating.value < 1 || editedCommentRating.value > 10) {
    alert('Escolha uma nota de 1 a 10 antes de atualizar')
    return
  }
  if (!editedCommentText.value.trim()) {
    alert('Digite um comentário antes de atualizar')
    return
  }

  try {
    await apiClient.patch(`/comentarios/${commentId}/`, {
      texto: editedCommentText.value,
      nota: editedCommentRating.value,
    })
    await fetchComments()
    cancelEditComment()
    alert('Comentário atualizado com sucesso!')
  } catch (err: any) {
    const msg = err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao atualizar comentário'
    alert(msg)
  }
}

const deleteComment = async (commentId: number) => {
  if (!confirm('Deseja realmente excluir este comentário?')) return

  try {
    await apiClient.delete(`/comentarios/${commentId}/`)
    await fetchComments()
    if (editingCommentId.value === commentId) cancelEditComment()
    alert('Comentário excluído com sucesso!')
  } catch (err: any) {
    const msg = err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao excluir comentário'
    alert(msg)
  }
}

const hoverControl = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, {
    opacity: hover ? '0.9' : '1'
  })
}

const hoverCard = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, {
    transform: hover ? 'translateY(-2px)' : 'translateY(0)'
  })
}

</script>

<template>
  <div style="width: 100%; max-width: 1600px; margin: 0 auto; padding: 0 40px;">
    <button @click="router.back()" style="margin-bottom: 30px; padding: 10px 20px; background-color: #f0f0f0; color: #333; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; transition: all 0.3s;" @mouseenter="setTargetStyle($event as MouseEvent, { backgroundColor: '#e0e0e0' })" @mouseleave="setTargetStyle($event as MouseEvent, { backgroundColor: '#f0f0f0' })">
      ← Voltar
    </button>

    <div v-if="loading" style="text-align: center; padding: 80px 40px;">
      <div style="display: inline-block; width: 50px; height: 50px; border: 4px solid #e5e7eb; border-top-color: #667eea; border-radius: 50%; animation: spin 1s linear infinite;"></div>
      <p style="margin-top: 20px; color: #666; font-size: 16px;">Carregando detalhes do filme...</p>
    </div>

    <div v-else-if="movie" style="display: grid; grid-template-columns: 350px 1fr; gap: 50px; align-items: start;">
      <div>
        <img 
          v-if="movie.poster_path"
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
          :alt="movie.title"
          style="width: 100%; border-radius: 12px; box-shadow: 0 10px 40px rgba(255, 245, 245, 0.2);"
        />
      </div>
      
      <div>
        <h1 style="font-size: 40px; font-weight: bold; margin-bottom: 16px; color: #ffffff;">{{ movie.title }}</h1>
        
        <div style="display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap;">
          <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 16px; border-radius: 8px; font-weight: bold;">⭐ {{ movie.vote_average?.toFixed(1) }}/10</div>
          <div style="background-color: #f0f0f0; color: #333; padding: 10px 16px; border-radius: 8px; font-weight: 500;">📅 {{ movie.release_date?.split('-')[0] }}</div>
          <div style="background-color: #f0f0f0; color: #333; padding: 10px 16px; border-radius: 8px; font-weight: 500;">⏱️ {{ movie.runtime }} min</div>
        </div>
        
        <h3 style="font-weight: bold; font-size: 18px; margin-bottom: 12px; color: #ffffff;">Gêneros</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 30px;">
          <span v-for="genre in movie.genres" :key="genre.id" style="background-color: #e5e7eb; color: #333; padding: 8px 14px; border-radius: 20px; font-size: 14px; font-weight: 500;">{{ genre.name }}</span>
        </div>
        
        <h3 style="font-weight: bold; font-size: 18px; margin-bottom: 12px; color: #ffffff;">Sinopse</h3>
        <p style="color: #ffffff; line-height: 1.8; font-size: 15px; margin-bottom: 40px;">{{ movie.overview || 'Sinopse não disponível' }}</p>
        <div style="margin-top: 50px;">
  <h2 style="color: white; margin-bottom: 20px;">💬 Comentários</h2>

  <div v-if="comments.length === 0" style="color: #aaa;">
    Nenhum comentário ainda
  </div>

  <div v-else style="display: flex; flex-direction: column; gap: 20px;">

    <div 
      v-for="c in comments" 
      :key="c.id"
      style="background: #1A1A2E; padding: 16px; border-radius: 10px;"
    >

      <!-- USUÁRIO E DATA -->
      <div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 12px; color: #aaa;">
        <span>👤 Usuário {{ c.usuario }}</span>
        <span>📅 {{ new Date(c.data_comentario).toLocaleDateString('pt-BR') }}</span>
      </div>

      <div v-if="editingCommentId === c.id" style="margin-bottom: 12px;">
        <textarea
          v-model="editedCommentText"
          style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; resize: vertical; min-height: 100px; margin-bottom: 12px;"
        ></textarea>

        <div style="display: flex; gap: 8px; margin-bottom: 12px;">
          <span
            v-for="star in 10"
            :key="`edit-${star}`"
            @click="editedCommentRating = star"
            :style="{
              fontSize: '20px',
              cursor: 'pointer',
              color: editedCommentRating >= star ? '#FFD700' : '#444'
            }"
          >
            ★
          </span>
        </div>

        <div style="display: flex; gap: 8px;">
          <button
            @click="updateComment(c.id)"
            style="background: #22c55e; color: white; padding: 8px 14px; border-radius: 8px; border: none; cursor: pointer;"
          >Salvar</button>
          <button
            @click="cancelEditComment"
            style="background: #ef4444; color: white; padding: 8px 14px; border-radius: 8px; border: none; cursor: pointer;"
          >Cancelar</button>
        </div>
      </div>

      <div v-else>
        <!-- TEXTO -->
        <p style="color: white; margin-bottom: 12px; line-height: 1.5;">
          {{ c.texto }}
        </p>

        <div v-if="c.nota" style="margin-bottom: 12px;">
          <span style="color: #aaa; font-size: 11px; margin-right: 8px;">Nota:</span>
          <span 
            v-for="i in 10" 
            :key="`nota-${c.id}-${i}`"
            :style="{
              color: i <= c.nota ? '#FFD700' : '#444',
              marginRight: '2px'
            }"
          >
            ★
          </span>
        </div>

        <div v-if="user?.id === c.usuario" style="display: flex; gap: 10px;">
          <button
            @click="startEditComment(c)"
            style="background: #3b82f6; color: white; padding: 6px 12px; border-radius: 8px; border: none; cursor: pointer;"
          >Editar</button>
          <button
            @click="deleteComment(c.id)"
            style="background: #ef4444; color: white; padding: 6px 12px; border-radius: 8px; border: none; cursor: pointer;"
          >Excluir</button>
        </div>
      </div>

    </div>

  </div>
</div>
        
        <template v-if="isLogged">
          <div style="display: flex; gap: 12px; margin-bottom: 30px;">
            <button 
              @click="toggleFavorite"
              :style="{
                background: isFavorite ? 'linear-gradient(135deg, #dc2626 0%, #991b1b 100%)' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '12px 20px',
                borderRadius: '8px',
                border: 'none',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s'
              }"
              @mouseenter="hoverControl($event, true)"
              @mouseleave="hoverControl($event, false)"
            >
              {{ isFavorite ? '❤️ Remover Favorito' : '🤍 Adicionar Favorito' }}
            </button>
            <button 
              @click="toggleWatchlist"
              :style="{
                background: isInWatchlist ? 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '12px 20px',
                borderRadius: '8px',
                border: 'none',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s'
              }"
              @mouseenter="hoverControl($event, true)"
              @mouseleave="hoverControl($event, false)"
            >
              {{ isInWatchlist ? '✅ Na Watchlist' : '📋 Adicionar Watchlist' }}
            </button>
          </div>

          <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); padding: 24px; border-radius: 12px; border-left: 4px solid #667eea; margin-bottom: 30px;">
            <h3 style="font-weight: bold; font-size: 18px; margin-bottom: 16px; color: #ffffff;">Avaliar e Comentar 🎬</h3>

            <div style="display: flex; gap: 8px; margin-bottom: 16px;">
              <span
                v-for="star in 10"
                :key="star"
                @click="setRating(star)"
                @mouseover="hoverRating = star"
                @mouseleave="hoverRating = 0"
                :style="{
                  fontSize: '28px',
                  cursor: 'pointer',
                  color: (hoverRating > 0 ? hoverRating : rating) >= star ? '#FFD700' : '#444',
                  transform: (hoverRating > 0 ? hoverRating : rating) >= star ? 'scale(1.2)' : 'scale(1)',
                  textShadow: (hoverRating > 0 ? hoverRating : rating) >= star ? '0 0 10px #FFD700' : 'none',
                  transition: 'all 0.2s'
                }"
              >
                ★
              </span>
            </div>

            <p style="color: #aaa; margin-bottom: 16px;">{{ rating ? `Sua nota: ${rating}/10` : 'Clique nas estrelas para avaliar' }}</p>

            <textarea
              v-model="comment"
              placeholder="Escreva seu comentário aqui..."
              style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; resize: vertical; min-height: 120px; margin-bottom: 16px;"
            ></textarea>

            <button
              @click="submitComment"
              :disabled="submitting || !comment.trim() || !rating"
              style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 20px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; transition: all 0.3s;"
              @mouseenter="hoverControl($event, true)"
              @mouseleave="hoverControl($event, false)"
            >
              {{ submitting ? 'Enviando...' : 'Enviar Avaliação + Comentário' }}
            </button>
          </div>
        </template>

        <template v-else>
          <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 24px; border-radius: 12px; border-left: 4px solid #667eea;">
            <p style="color: #667eea; font-weight: 600; margin-bottom: 12px;">Quer ver as opiniões de outros usuários?</p>
            <router-link to="/login" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; transition: opacity 0.3s;" @mouseenter="hoverControl($event, true)" @mouseleave="hoverControl($event, false)">
              🔓 Faça Login
            </router-link>
          </div>
        </template>
      </div>
    </div>

    <div v-else style="text-align: center; padding: 80px 40px;">
      <p style="font-size: 18px; color: #666;">📽️ Filme não encontrado</p>
    </div>
  </div>
</template>

<style>
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
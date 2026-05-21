<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { TMDB_API_KEY, TMDB_BASE_URL } from '../utils/api'
import { apiClient } from '../utils/axiosConfig'

const route = useRoute()
const router = useRouter()
const { isLogged, user } = useAuth()

const movie = ref<any>(null)
const loading = ref(false)
const isFavorite = ref(false)
const isInWatchlist = ref(false)
const rating = ref(0)
const comment = ref('')
const hoverRating = ref(0)
const submitting = ref(false)
const comments = ref<any[]>([])
const editingCommentId = ref<number | null>(null)
const editedCommentText = ref('')
const editedCommentRating = ref(0)

const setRating = (value: number) => { rating.value = value }

onMounted(async () => {
  loading.value = true
  try {
    const movieId = route.params.id
    const response = await axios.get(`${TMDB_BASE_URL}/movie/${movieId}?api_key=${TMDB_API_KEY}&language=pt-BR`)
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

const fetchComments = async () => {
  try {
    const { data } = await apiClient.get(`/comentarios/?filme=${route.params.id}`)
    comments.value = data.results ? data.results : (Array.isArray(data) ? data : [])
  } catch (err: any) {
    if (err.response?.status !== 401) console.error(err)
    comments.value = []
  }
}

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

const toggleFavorite = async () => {
  if (!isLogged.value) { alert('Faça login para adicionar ou remover favoritos'); router.push('/login'); return }
  try {
    if (isFavorite.value) {
      const { data } = await apiClient.get(`/favoritos/?filme=${route.params.id}`)
      const favList = data.results ? data.results : (Array.isArray(data) ? data : [])
      if (favList[0]?.id) await apiClient.delete(`/favoritos/${favList[0].id}/`)
    } else {
      await apiClient.post('/favoritos/', { filme_id: route.params.id, titulo: movie.value.title, poster: movie.value.poster_path || '' })
    }
    isFavorite.value = !isFavorite.value
  } catch (err: any) {
    alert(err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao atualizar favorito')
  }
}

const toggleWatchlist = async () => {
  if (!isLogged.value) { alert('Faça login para adicionar ou remover da watchlist'); router.push('/login'); return }
  try {
    if (isInWatchlist.value) {
      const { data } = await apiClient.get(`/watchlist/?filme=${route.params.id}`)
      const wlList = data.results ? data.results : (Array.isArray(data) ? data : [])
      if (wlList[0]?.id) await apiClient.delete(`/watchlist/${wlList[0].id}/`)
    } else {
      await apiClient.post('/watchlist/', { filme_id: route.params.id, titulo: movie.value.title, poster: movie.value.poster_path || '' })
    }
    isInWatchlist.value = !isInWatchlist.value
  } catch (err: any) {
    alert(err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao atualizar watchlist')
  }
}

const submitComment = async () => {
  if (!rating.value || rating.value < 1 || rating.value > 10) { alert('Escolha uma nota de 1 a 10'); return }
  if (!comment.value.trim()) { alert('Digite um comentário'); return }
  submitting.value = true
  try {
    const existing = comments.value.find((c: any) => c.usuario === user.value?.id)
    if (existing) {
      await apiClient.patch(`/comentarios/${existing.id}/`, { texto: comment.value, nota: rating.value })
      alert('Comentário atualizado!')
    } else {
      await apiClient.post('/comentarios/', { filme_id: route.params.id, texto: comment.value, titulo: movie.value.title, nota: rating.value })
      alert('Avaliação enviada!')
    }
    comment.value = ''; rating.value = 0; hoverRating.value = 0
    await fetchComments()
  } catch (err: any) {
    alert(err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao registrar comentário')
  } finally {
    submitting.value = false
  }
}

const startEditComment = (c: any) => {
  editingCommentId.value = c.id; editedCommentText.value = c.texto; editedCommentRating.value = c.nota || 0
}
const cancelEditComment = () => { editingCommentId.value = null; editedCommentText.value = ''; editedCommentRating.value = 0 }

const updateComment = async (commentId: number) => {
  if (!editedCommentRating.value) { alert('Escolha uma nota'); return }
  if (!editedCommentText.value.trim()) { alert('Digite um comentário'); return }
  try {
    await apiClient.patch(`/comentarios/${commentId}/`, { texto: editedCommentText.value, nota: editedCommentRating.value })
    await fetchComments(); cancelEditComment(); alert('Comentário atualizado!')
  } catch (err: any) {
    alert(err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao atualizar')
  }
}

const deleteComment = async (commentId: number) => {
  if (!confirm('Deseja excluir este comentário?')) return
  try {
    await apiClient.delete(`/comentarios/${commentId}/`)
    await fetchComments()
    if (editingCommentId.value === commentId) cancelEditComment()
    alert('Comentário excluído!')
  } catch (err: any) {
    alert(err.response?.data ? JSON.stringify(err.response.data) : err.message || 'Erro ao excluir')
  }
}
</script>

<template>
  <div class="mx-auto px-4" style="max-width:1600px">
    <button @click="router.back()" class="btn btn-outline-secondary mb-4 fw-medium">← Voltar</button>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="mf-spinner"></div>
      <p class="mt-3" style="color:#9ca3af">Carregando detalhes do filme...</p>
    </div>

    <!-- Conteúdo -->
    <div v-else-if="movie" class="row g-5 align-items-start">

      <!-- Poster -->
      <div class="col-12 col-md-4 col-lg-3">
        <img
          v-if="movie.poster_path"
          :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
          :alt="movie.title"
          class="w-100 rounded-3 shadow-lg"
        />
      </div>

      <!-- Info -->
      <div class="col-12 col-md-8 col-lg-9">
        <h1 class="fw-bold text-white mb-3" style="font-size:clamp(24px,3vw,40px)">{{ movie.title }}</h1>

        <!-- Badges de info -->
        <div class="d-flex flex-wrap gap-2 mb-4">
          <span class="badge px-3 py-2 fw-bold" style="background:linear-gradient(135deg,#667eea,#764ba2)">⭐ {{ movie.vote_average?.toFixed(1) }}/10</span>
          <span class="badge px-3 py-2 fw-medium" style="background:#2a2a45;color:#e5e7eb">📅 {{ movie.release_date?.split('-')[0] }}</span>
          <span class="badge px-3 py-2 fw-medium" style="background:#2a2a45;color:#e5e7eb">⏱️ {{ movie.runtime }} min</span>
        </div>

        <!-- Gêneros -->
        <h3 class="fw-bold text-white mb-2" style="font-size:17px">Gêneros</h3>
        <div class="d-flex flex-wrap gap-2 mb-4">
          <span v-for="genre in movie.genres" :key="genre.id" class="badge rounded-pill px-3 py-2" style="background:#2a2a45;color:#e5e7eb">
            {{ genre.name }}
          </span>
        </div>

        <!-- Sinopse -->
        <h3 class="fw-bold text-white mb-2" style="font-size:17px">Sinopse</h3>
        <p class="mb-5 text-white lh-lg">{{ movie.overview || 'Sinopse não disponível' }}</p>

        <!-- Botões ação (logado) -->
        <template v-if="isLogged">
          <div class="d-flex flex-wrap gap-3 mb-4">
            <button
              @click="toggleFavorite"
              class="btn fw-semibold px-4 py-2"
              :style="{ background: isFavorite ? 'linear-gradient(135deg,#dc2626,#991b1b)' : 'linear-gradient(135deg,#667eea,#764ba2)', color:'white', border:'none', borderRadius:'8px' }"
            >
              {{ isFavorite ? '❤️ Remover Favorito' : '🤍 Adicionar Favorito' }}
            </button>
            <button
              @click="toggleWatchlist"
              class="btn fw-semibold px-4 py-2"
              :style="{ background: isInWatchlist ? 'linear-gradient(135deg,#2563eb,#1e40af)' : 'linear-gradient(135deg,#667eea,#764ba2)', color:'white', border:'none', borderRadius:'8px' }"
            >
              {{ isInWatchlist ? '✅ Na Watchlist' : '📋 Adicionar Watchlist' }}
            </button>
          </div>

          <!-- Avaliar -->
          <div class="p-4 mb-4 rounded-3" style="background:linear-gradient(135deg,rgba(102,126,234,0.1),rgba(118,75,162,0.1));border-left:4px solid #667eea">
            <h3 class="fw-bold text-white mb-3">Avaliar e Comentar 🎬</h3>
            <div class="d-flex gap-1 mb-2">
              <span
                v-for="star in 10" :key="star"
                @click="setRating(star)" @mouseover="hoverRating = star" @mouseleave="hoverRating = 0"
                class="user-select-none"
                :style="{
                  fontSize:'28px', cursor:'pointer',
                  color: (hoverRating > 0 ? hoverRating : rating) >= star ? '#FFD700' : '#444',
                  transform: (hoverRating > 0 ? hoverRating : rating) >= star ? 'scale(1.2)' : 'scale(1)',
                  transition: 'all 0.2s'
                }"
              >★</span>
            </div>
            <p class="mb-3" style="color:#9ca3af">{{ rating ? `Sua nota: ${rating}/10` : 'Clique nas estrelas para avaliar' }}</p>
            <textarea
              v-model="comment"
              class="form-control mb-3"
              placeholder="Escreva seu comentário aqui..."
              rows="4"
            ></textarea>
            <button
              @click="submitComment"
              :disabled="submitting || !comment.trim() || !rating"
              class="btn fw-semibold px-4 py-2"
              style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:8px"
            >
              {{ submitting ? 'Enviando...' : 'Enviar Avaliação + Comentário' }}
            </button>
          </div>
        </template>

        <!-- CTA não logado -->
        <template v-else>
          <div class="p-4 mb-4 rounded-3" style="background:linear-gradient(135deg,rgba(102,126,234,0.1),rgba(118,75,162,0.1));border-left:4px solid #667eea">
            <p class="fw-semibold mb-3" style="color:#667eea">Quer interagir com este filme?</p>
            <router-link to="/login" class="btn fw-semibold px-4 py-2" style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:8px">
              🔓 Faça Login
            </router-link>
          </div>
        </template>

        <!-- Comentários -->
        <h2 class="fw-bold text-white mb-3">💬 Comentários</h2>
        <div v-if="comments.length === 0" style="color:#9ca3af">Nenhum comentário ainda</div>
        <div class="d-flex flex-column gap-3">
          <div v-for="c in comments" :key="c.id" class="p-3 rounded-3" style="background:#1A1A2E">
            <div class="d-flex justify-content-between mb-2" style="font-size:12px;color:#9ca3af">
              <span>👤 Usuário {{ c.usuario }}</span>
              <span>📅 {{ new Date(c.data_comentario).toLocaleDateString('pt-BR') }}</span>
            </div>

            <!-- Edição inline -->
            <div v-if="editingCommentId === c.id">
              <textarea v-model="editedCommentText" class="form-control mb-2" rows="3"></textarea>
              <div class="d-flex gap-1 mb-2">
                <span
                  v-for="star in 10" :key="`edit-${star}`"
                  @click="editedCommentRating = star"
                  :style="{ fontSize:'20px', cursor:'pointer', color: editedCommentRating >= star ? '#FFD700' : '#444' }"
                >★</span>
              </div>
              <div class="d-flex gap-2">
                <button @click="updateComment(c.id)" class="btn btn-sm btn-success fw-semibold">Salvar</button>
                <button @click="cancelEditComment" class="btn btn-sm btn-danger fw-semibold">Cancelar</button>
              </div>
            </div>

            <div v-else>
              <p class="text-white mb-2 lh-base">{{ c.texto }}</p>
              <div v-if="c.nota" class="mb-2">
                <span style="color:#9ca3af;font-size:11px;margin-right:8px">Nota:</span>
                <span v-for="i in 10" :key="`nota-${c.id}-${i}`" :style="{ color: i <= c.nota ? '#FFD700' : '#444' }">★</span>
              </div>
              <div v-if="user?.id === c.usuario" class="d-flex gap-2">
                <button @click="startEditComment(c)" class="btn btn-sm btn-primary fw-semibold">Editar</button>
                <button @click="deleteComment(c.id)" class="btn btn-sm btn-danger fw-semibold">Excluir</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Não encontrado -->
    <div v-else class="text-center py-5">
      <p class="fs-5" style="color:#9ca3af">📽️ Filme não encontrado</p>
    </div>
  </div>
</template>

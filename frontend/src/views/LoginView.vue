<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { apiClient } from '../utils/axiosConfig'

const router = useRouter()
const { login } = useAuth()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (!email.value || !password.value) {
    error.value = 'Email e senha são obrigatórios'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const response = await apiClient.post('/usuarios/login/', {
      email: email.value,
      password: password.value,
    })
    login(response.data.user, response.data.access, response.data.refresh)
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Email ou senha incorretos'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height:70vh">
    <div class="card shadow-lg p-4 p-md-5" style="width:100%;max-width:420px;background:#1e1e30;border-color:#2a2a45">
      <h1 class="fw-bold text-center mb-1 text-white" style="font-size:28px">Bem-vindo de volta</h1>
      <p class="text-center mb-4" style="color:#9ca3af">Faça login na sua conta</p>

      <div v-if="error" class="alert mb-4 p-3" style="background:linear-gradient(135deg,#fee2e2,#fecaca);border-left:4px solid #dc2626;color:#991b1b;border-radius:8px;font-weight:500">
        ⚠️ {{ error }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" placeholder="seu@email.com" />
        </div>
        <div class="mb-4">
          <label class="form-label">Senha</label>
          <input v-model="password" type="password" class="form-control" placeholder="Sua senha" />
        </div>
        <button type="submit" :disabled="loading" class="btn btn-mf-primary w-100 py-2 fw-bold fs-6">
          {{ loading ? '⏳ Entrando...' : '🔓 Entrar' }}
        </button>
      </form>

      <p class="mt-4 text-center" style="color:#9ca3af">
        Não tem conta?
        <router-link to="/register" class="fw-semibold" style="color:#667eea">Cadastre-se aqui</router-link>
      </p>
    </div>
  </div>
</template>

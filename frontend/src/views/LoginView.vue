<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { setTargetStyle } from '../composables/useHoverStyle'
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

    console.log('RESPOSTA LOGIN:', response.data)

    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // Usar composable para salvar e atualizar estado
    login(response.data.user, response.data.access)

    // Redirecionar para home
    router.push('/')
  } catch (err: any) {
    if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else {
      error.value = 'Email ou senha incorretos'
    }
  } finally {
    loading.value = false
  }
}

const inputFocus = (event: FocusEvent) => {
  setTargetStyle(event, {
    borderColor: '#667eea',
    boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
  })
}

const inputBlur = (event: FocusEvent) => {
  setTargetStyle(event, {
    borderColor: '#e5e7eb',
    boxShadow: 'none'
  })
}

const controlHover = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, {
    opacity: hover ? (loading.value ? '0.7' : '0.9') : '1'
  })
}

const linkHover = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, {
    color: hover ? '#764ba2' : '#667eea'
  })
}
</script>

<template>
  <div style="width: 100%; display: flex; justify-content: center; align-items: center; min-height: 100%;">
    <div style="background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); padding: 40px; width: 100%; max-width: 400px;">
      <h1 style="font-size: 32px; font-weight: bold; margin-bottom: 8px;color: #333; text-align: center;">Bem-vindo de volta</h1>
      <p style="text-align: center; color: #666; margin-bottom: 30px;">Faça login na sua conta</p>

      <div v-if="error" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border-left: 4px solid #dc2626; color: #991b1b; padding: 14px; margin-bottom: 20px; border-radius: 8px; font-weight: 500;">
        ⚠️ {{ error }}
      </div>

      <form @submit.prevent="handleLogin">
        <div style="margin-bottom: 20px;">
          <label style="display: block; color: #1a202c; font-weight: 600; margin-bottom: 8px;">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="seu@email.com"
            style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; transition: border-color 0.3s, box-shadow 0.3s;"
            @focus="inputFocus"
            @blur="inputBlur"
          />
        </div>

        <div style="margin-bottom: 30px;">
          <label style="display: block; color: #1a202c; font-weight: 600; margin-bottom: 8px;">Senha</label>
          <input
            v-model="password"
            type="password"
            placeholder="Sua senha"
            style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; transition: border-color 0.3s, box-shadow 0.3s;"
            @focus="inputFocus"
            @blur="inputBlur"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          style="width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; transition: opacity 0.3s;"
          @mouseenter="controlHover($event, true)"
          @mouseleave="controlHover($event, false)"
        >
          {{ loading ? '⏳ Entrando...' : '🔓 Entrar' }}
        </button>
      </form>

      <p style="margin-top: 20px; text-align: center; color: #666;">
        Não tem conta?
        <router-link to="/register" style="color: #667eea; text-decoration: none; font-weight: 600; transition: color 0.3s;" @mouseenter="(e) => setTargetStyle(e as MouseEvent, { color: '#764ba2' })" @mouseleave="(e) => setTargetStyle(e as MouseEvent, { color: '#667eea' })">Cadastre-se aqui</router-link>
      </p>
    </div>
  </div>
</template>
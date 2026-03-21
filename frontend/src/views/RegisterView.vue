<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { setTargetStyle } from '../composables/useHoverStyle'
import { apiClient } from '../utils/axiosConfig'

const router = useRouter()
const nome = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

const handleRegister = async () => {
  if (!nome.value || !email.value || !password.value || !confirmPassword.value) {
    error.value = 'Todos os campos são obrigatórios'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'As senhas não conferem'
    return
  }

  if (password.value.length < 6) {
    error.value = 'A senha deve ter pelo menos 6 caracteres'
    return
  }

  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const response = await apiClient.post('/usuarios/cadastro/', {
      nome: nome.value,
      email: email.value,
      password: password.value,
      confirmPassword: confirmPassword.value,
    })

    success.value = 'Cadastro realizado com sucesso! Redirecionando para login...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err: any) {
    if (err.response?.data?.email) {
      error.value = err.response.data.email[0]
    } else if (err.response?.data?.password) {
      error.value = err.response.data.password[0]
    } else if (err.response?.data?.error) {
      error.value = err.response.data.error
    } else {
      error.value = 'Erro ao cadastrar. Tente novamente.'
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

const buttonHover = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, {
    opacity: hover ? (loading.value ? '0.7' : '0.9') : '1'
  })
}

const linkHover = (event: MouseEvent, hover: boolean) => {
  setTargetStyle(event, { color: hover ? '#764ba2' : '#667eea' })
}
</script>

<template>
  <div style="width: 100%; display: flex; justify-content: center; align-items: center; min-height: 100%;">
    <div style="background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); padding: 40px; width: 100%; max-width: 400px;">
      <h1 style="font-size: 32px; font-weight: bold; margin-bottom: 8px;color: #333;  text-align: center;">Criar Conta</h1>
      <p style="text-align: center; color: #333; margin-bottom: 30px;">Junte-se ao MovieFlix today</p>

      <div v-if="error" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border-left: 4px solid #dc2626; color: #991b1b; padding: 14px; margin-bottom: 20px; border-radius: 8px; font-weight: 500;">
        ⚠️ {{ error }}
      </div>

      <div v-if="success" style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); border-left: 4px solid #16a34a; color: #166534; padding: 14px; margin-bottom: 20px; border-radius: 8px; font-weight: 500;">
        ✅ {{ success }}
      </div>

      <form @submit.prevent="handleRegister" v-if="!success">
        <div style="margin-bottom: 20px;">
          <label style="display: block; color: #1a202c; font-weight: 600; margin-bottom: 8px;">Nome Completo</label>
          <input
            v-model="nome"
            type="text"
            placeholder="Seu nome"
            style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; transition: border-color 0.3s, box-shadow 0.3s;"
            @focus="inputFocus"
            @blur="inputBlur"
          />
        </div>

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

        <div style="margin-bottom: 20px;">
          <label style="display: block; color: #1a202c; font-weight: 600; margin-bottom: 8px;">Senha</label>
          <input
            v-model="password"
            type="password"
            placeholder="Mínimo 6 caracteres"
            style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; transition: border-color 0.3s, box-shadow 0.3s;"
            @focus="inputFocus"
            @blur="inputBlur"
          />
        </div>

        <div style="margin-bottom: 30px;">
          <label style="display: block; color: #1a202c; font-weight: 600; margin-bottom: 8px;">Confirmar Senha</label>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Confirme sua senha"
            style="width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; transition: border-color 0.3s, box-shadow 0.3s;"
            @focus="inputFocus"
            @blur="inputBlur"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          style="width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; transition: opacity 0.3s;"
          @mouseenter="buttonHover($event, true)"
          @mouseleave="buttonHover($event, false)"
        >
          {{ loading ? '⏳ Cadastrando...' : '✨ Cadastrar' }}
        </button>
      </form>

      <p style="margin-top: 20px; text-align: center; color: #666;">
        Já tem conta?
        <router-link to="/login" style="color: #667eea; text-decoration: none; font-weight: 600; transition: color 0.3s;" @mouseenter="linkHover($event, true)" @mouseleave="linkHover($event, false)">Faça login</router-link>
      </p>
    </div>
  </div>
</template>
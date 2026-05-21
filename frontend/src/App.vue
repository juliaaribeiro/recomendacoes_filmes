<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuth } from './composables/useAuth'

const { isLogged, user, logout } = useAuth()

function handleLogout() {
  const confirmLogout = confirm("Tem certeza que deseja sair?")
  if (confirmLogout) {
    logout()
  }
}
</script>

<template>
  <div id="app" data-bs-theme="dark">

    <!-- HEADER -->
    <header
      class="sticky-top py-2"
      :style="{
        backdropFilter: 'blur(12px)',
        background: isLogged
          ? 'linear-gradient(135deg, rgba(0,198,255,0.2), rgba(123,47,247,0.25))'
          : 'rgba(15,15,27,0.82)',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        transition: 'all 0.4s ease',
        zIndex: 100
      }"
    >
      <div class="d-flex justify-content-between align-items-center mx-auto px-4" style="max-width:1600px">

        <router-link to="/" class="d-flex align-items-center gap-2 text-decoration-none">
          <span style="font-size:28px">🎬</span>
          <span class="fw-bold fs-4 mf-gradient-text">MovieFlix</span>
        </router-link>

        <nav class="d-flex align-items-center gap-3">
          <router-link to="/" class="fw-semibold">Home</router-link>
          <router-link to="/search" class="fw-semibold">Buscar</router-link>

          <template v-if="isLogged">
            <router-link to="/meus-favoritos">❤️ Favoritos</router-link>
            <router-link to="/minha-watchlist">📋 Watchlist</router-link>
            <router-link
              v-if="user?.tipo_usuario === 'admin' || user?.is_staff"
              to="/admin-dashboard"
              class="btn btn-sm btn-mf-primary px-3"
            >
              ⚙️ Admin
            </router-link>

            <!-- Usuário logado -->
            <div
              class="d-flex align-items-center gap-2 ms-3 px-3 py-2 rounded-pill"
              style="backdrop-filter:blur(10px); background:linear-gradient(135deg,rgba(0,198,255,0.25),rgba(123,47,247,0.3)); border:1px solid rgba(255,255,255,0.15); box-shadow:0 0 12px rgba(0,198,255,0.25);"
            >
              <div
                class="d-flex align-items-center justify-content-center rounded-circle fw-bold text-white"
                style="width:32px;height:32px;background:linear-gradient(135deg,#00C6FF,#7B2FF7)"
              >
                {{ user?.nome?.substring(0,1) || 'U' }}
              </div>
              <span style="font-size:13px;font-weight:600">{{ user?.nome }}</span>
              <button @click="handleLogout" class="btn btn-sm btn-mf-primary px-3">Sair</button>
            </div>
          </template>

          <template v-else>
            <router-link to="/login" class="btn btn-sm btn-mf-primary px-4 py-2">Login</router-link>
          </template>
        </nav>
      </div>
    </header>

    <main class="flex-grow-1 py-5 px-3">
      <RouterView />
    </main>

    <footer class="py-3 text-center" style="background:#1a202c;color:#a0aec0;">
      <p class="mb-0" style="font-size:13px">&copy; 2026 MovieFlix</p>
    </footer>
  </div>
</template>
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
  <div id="app" style="display: flex; flex-direction: column; min-height: 100vh; background: radial-gradient(circle at top, #1A1A2E, #0F0F1B); color: #E5E7EB; overflow-x: hidden;">
    
    <!-- HEADER -->
    <header 
      :style="{
        position: 'sticky',
        top: '0',
        zIndex: '100',
        backdropFilter: 'blur(12px)',
        background: isLogged 
          ? 'linear-gradient(135deg, rgba(0,198,255,0.2), rgba(123,47,247,0.25))'
          : 'rgba(15, 15, 27, 0.64)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '12px 0',
        transition: 'all 0.4s ease'
      }"
    >
      <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1600px; width: 100%; margin: 0 auto; padding: 0 32px;">
        
        <router-link to="/" style="font-size: 26px; font-weight: 800; color: white; text-decoration: none; display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 28px;">🎬</span>
          <span style="background: linear-gradient(135deg, #FF3CAC, #00C6FF); -webkit-background-clip: text; color: transparent;">
            MovieFlix
          </span>
        </router-link>

        <nav style="display: flex; gap: 20px; align-items: center;">
          <router-link to="/" style="font-weight: 600;">Home</router-link>
          <router-link to="/search" style="font-weight: 600;">Buscar</router-link>

          <template v-if="isLogged">
            <router-link to="/meus-favoritos">❤️ Favoritos</router-link>
            <router-link to="/minha-watchlist">📋 Watchlist</router-link>

            <!-- BLOCO DO USUÁRIO (AGORA COM GLASS IGUAL AO HEADER) -->
            <div 
              style="
                margin-left: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 8px 14px;
                border-radius: 999px;
                backdrop-filter: blur(10px);
                background: linear-gradient(135deg, rgba(0,198,255,0.25), rgba(123,47,247,0.3));
                border: 1px solid rgba(255,255,255,0.15);
                box-shadow: 0 0 12px rgba(0,198,255,0.25);
                transition: all 0.3s ease;
              "
            >
              
              <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #00C6FF, #7B2FF7); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                {{ user?.nome?.substring(0,1) || 'U' }}
              </div>

              <span style="font-size: 13px; font-weight: 600;">
                {{ user?.nome }}
              </span>

              <button 
                @click="handleLogout"
                style="background: linear-gradient(135deg, #FF3CAC, #7B2FF7); color: white; padding: 6px 12px; border: none; border-radius: 999px; font-weight: 700; cursor: pointer;"
              >
                Sair
              </button>
            </div>
          </template>

          <template v-else>
            <router-link 
              to="/login" 
              style="background: linear-gradient(135deg, #FF3CAC, #7B2FF7); color: white; padding: 8px 18px; border-radius: 999px; font-weight: 700;"
            >
              Login
            </router-link>
          </template>
        </nav>
      </div>
    </header>

    <main style="flex: 1; padding: 40px 20px;">
      <RouterView />
    </main>

    <footer style="background-color: #1a202c; color: #a0aec0; padding: 16px; text-align: center;">
      <p style="font-size: 13px;">&copy; 2026 MovieFlix</p>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

#app {
  font-family: 'Poppins', sans-serif;
}

a {
  color: #E5E7EB;
  text-decoration: none;
}
</style>
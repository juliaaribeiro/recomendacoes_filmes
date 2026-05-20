<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { apiClient } from '../utils/axiosConfig'

const router = useRouter()
const { user, isLogged } = useAuth()

const stats = ref<any>(null)
const loading = ref(true)
const error = ref('')
const activeTab = ref<'overview' | 'usuarios' | 'conteudo'>('overview')

onMounted(async () => {
  if (!isLogged.value) {
    router.push('/login')
    return
  }
  await fetchStats()
})

const fetchStats = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await apiClient.get('/admin-stats/')
    stats.value = data
  } catch (err: any) {
    error.value = 'Erro ao carregar estatísticas. Verifique se você tem permissão de administrador.'
  } finally {
    loading.value = false
  }
}

const maxCadastros = computed(() => {
  if (!stats.value) return 1
  return Math.max(...stats.value.usuarios.cadastros_por_dia.map((d: any) => d.total), 1)
})

const taxaAssistidos = computed(() => {
  if (!stats.value || stats.value.watchlist.total === 0) return 0
  return Math.round((stats.value.watchlist.assistidos / stats.value.watchlist.total) * 100)
})

const formatDate = (dateStr: string) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}
</script>

<template>
  <div class="admin-root">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">🎬</span>
        <div>
          <div class="logo-title">MovieFlix</div>
          <div class="logo-sub">Painel Admin</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <button :class="['nav-item', activeTab === 'overview' && 'active']" @click="activeTab = 'overview'">
          <span>📊</span> Visão Geral
        </button>
        <button :class="['nav-item', activeTab === 'usuarios' && 'active']" @click="activeTab = 'usuarios'">
          <span>👥</span> Usuários
        </button>
        <button :class="['nav-item', activeTab === 'conteudo' && 'active']" @click="activeTab = 'conteudo'">
          <span>🎥</span> Conteúdo
        </button>
      </nav>

      <div class="sidebar-footer">
        <div class="admin-badge">
          <span>⚙️</span>
          <div>
            <div class="admin-name">{{ user?.nome || user?.email }}</div>
            <div class="admin-role">Administrador</div>
          </div>
        </div>
        <button class="btn-voltar" @click="router.push('/')">← Voltar ao site</button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="main-content">
      <!-- Loading -->
      <div v-if="loading" class="center-state">
        <div class="spinner"></div>
        <p>Carregando dados...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="center-state error-state">
        <div style="font-size:48px">⚠️</div>
        <p>{{ error }}</p>
        <button class="btn-primary" @click="fetchStats">Tentar novamente</button>
      </div>

      <template v-else-if="stats">

        <!-- VISÃO GERAL -->
        <div v-if="activeTab === 'overview'">
          <div class="page-header">
            <h1>Visão Geral</h1>
            <button class="btn-refresh" @click="fetchStats">↻ Atualizar</button>
          </div>

          <!-- Cards principais -->
          <div class="cards-grid">
            <div class="stat-card blue">
              <div class="stat-icon">👥</div>
              <div class="stat-value">{{ stats.usuarios.total }}</div>
              <div class="stat-label">Usuários cadastrados</div>
              <div class="stat-sub">+{{ stats.usuarios.hoje }} hoje</div>
            </div>
            <div class="stat-card purple">
              <div class="stat-icon">💬</div>
              <div class="stat-value">{{ stats.comentarios.total }}</div>
              <div class="stat-label">Comentários</div>
              <div class="stat-sub">Nota média: ⭐ {{ stats.comentarios.media_nota }}/10</div>
            </div>
            <div class="stat-card red">
              <div class="stat-icon">❤️</div>
              <div class="stat-value">{{ stats.favoritos.total }}</div>
              <div class="stat-label">Favoritos</div>
              <div class="stat-sub">+{{ stats.favoritos.ultimos_7_dias }} esta semana</div>
            </div>
            <div class="stat-card green">
              <div class="stat-icon">📋</div>
              <div class="stat-value">{{ stats.watchlist.total }}</div>
              <div class="stat-label">Watchlist</div>
              <div class="stat-sub">{{ taxaAssistidos }}% assistidos</div>
            </div>
          </div>

          <!-- Gráfico de cadastros -->
          <div class="section-card">
            <h2>📈 Cadastros nos últimos 7 dias</h2>
            <div class="bar-chart">
              <div
                v-for="dia in stats.usuarios.cadastros_por_dia"
                :key="dia.dia"
                class="bar-col"
              >
                <div class="bar-value">{{ dia.total }}</div>
                <div
                  class="bar-fill"
                  :style="{ height: `${Math.max((dia.total / maxCadastros) * 100, 4)}%` }"
                ></div>
                <div class="bar-label">{{ dia.dia }}</div>
              </div>
            </div>
          </div>

          <!-- Watchlist progress -->
          <div class="section-card">
            <h2>📋 Status da Watchlist</h2>
            <div class="progress-row">
              <span>Assistidos ({{ stats.watchlist.assistidos }})</span>
              <div class="progress-bar">
                <div class="progress-fill green-fill" :style="{ width: taxaAssistidos + '%' }"></div>
              </div>
              <span>{{ taxaAssistidos }}%</span>
            </div>
            <div class="progress-row">
              <span>Pendentes ({{ stats.watchlist.pendentes }})</span>
              <div class="progress-bar">
                <div class="progress-fill gray-fill" :style="{ width: (100 - taxaAssistidos) + '%' }"></div>
              </div>
              <span>{{ 100 - taxaAssistidos }}%</span>
            </div>
          </div>
        </div>

        <!-- USUÁRIOS -->
        <div v-if="activeTab === 'usuarios'">
          <div class="page-header">
            <h1>Usuários</h1>
          </div>

          <div class="cards-grid">
            <div class="stat-card blue">
              <div class="stat-icon">👥</div>
              <div class="stat-value">{{ stats.usuarios.total }}</div>
              <div class="stat-label">Total</div>
            </div>
            <div class="stat-card purple">
              <div class="stat-icon">📅</div>
              <div class="stat-value">{{ stats.usuarios.ultimos_7_dias }}</div>
              <div class="stat-label">Últimos 7 dias</div>
            </div>
            <div class="stat-card green">
              <div class="stat-icon">🟢</div>
              <div class="stat-value">{{ stats.usuarios.ativos_semana }}</div>
              <div class="stat-label">Ativos esta semana</div>
            </div>
            <div class="stat-card orange">
              <div class="stat-icon">🗓️</div>
              <div class="stat-value">{{ stats.usuarios.ultimos_30_dias }}</div>
              <div class="stat-label">Últimos 30 dias</div>
            </div>
          </div>

          <div class="section-card">
            <h2>👤 Usuários recentes</h2>
            <table class="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Tipo</th>
                  <th>Cadastro</th>
                  <th>Último login</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="u in stats.usuarios.recentes" :key="u.id">
                  <td class="muted">{{ u.id }}</td>
                  <td>{{ u.nome || '—' }}</td>
                  <td class="muted">{{ u.email }}</td>
                  <td>
                    <span :class="['tipo-badge', u.tipo_usuario === 'admin' ? 'admin' : 'user']">
                      {{ u.tipo_usuario || 'user' }}
                    </span>
                  </td>
                  <td class="muted">{{ formatDate(u.data_criacao) }}</td>
                  <td class="muted">{{ formatDate(u.last_login) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- CONTEÚDO -->
        <div v-if="activeTab === 'conteudo'">
          <div class="page-header">
            <h1>Conteúdo</h1>
          </div>

          <div class="two-cols">
            <div class="section-card">
              <h2>❤️ Filmes mais favoritados</h2>
              <div v-if="stats.favoritos.top_filmes.length === 0" class="empty">Nenhum dado ainda</div>
              <div v-for="(filme, i) in stats.favoritos.top_filmes" :key="filme.filme_id" class="rank-item">
                <span class="rank-num">{{ Number(i) + 1 }}</span>
                <span class="rank-title">{{ filme.titulo || `Filme #${filme.filme_id}` }}</span>
                <span class="rank-count">{{ filme.total }} ❤️</span>
              </div>
            </div>

            <div class="section-card">
              <h2>💬 Filmes mais comentados</h2>
              <div v-if="stats.watchlist.top_filmes.length === 0" class="empty">Nenhum dado ainda</div>
              <div v-for="(filme, i) in stats.watchlist.top_filmes" :key="filme.filme_id" class="rank-item">
                <span class="rank-num">{{ Number(i) + 1 }}</span>
                <span class="rank-title">{{ filme.titulo || `Filme #${filme.filme_id}` }}</span>
                <span class="rank-count">{{ filme.total }} 💬</span>
              </div>
            </div>
          </div>

          <div class="section-card">
            <h2>💬 Comentários</h2>
            <div class="cards-grid" style="margin-top:16px">
              <div class="stat-card purple">
                <div class="stat-icon">💬</div>
                <div class="stat-value">{{ stats.comentarios.total }}</div>
                <div class="stat-label">Total</div>
              </div>
              <div class="stat-card blue">
                <div class="stat-icon">📅</div>
                <div class="stat-value">{{ stats.comentarios.hoje }}</div>
                <div class="stat-label">Hoje</div>
              </div>
              <div class="stat-card green">
                <div class="stat-icon">⭐</div>
                <div class="stat-value">{{ stats.comentarios.media_nota }}</div>
                <div class="stat-label">Nota média /10</div>
              </div>
              <div class="stat-card orange">
                <div class="stat-icon">📆</div>
                <div class="stat-value">{{ stats.comentarios.ultimos_7_dias }}</div>
                <div class="stat-label">Últimos 7 dias</div>
              </div>
            </div>
          </div>
        </div>

      </template>
    </main>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.admin-root {
  display: flex;
  min-height: 100vh;
  background: #0d0d14;
  color: #e8e6f0;
  font-family: 'DM Sans', sans-serif;
}

/* SIDEBAR */
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: #13131f;
  border-right: 1px solid #1e1e30;
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  position: sticky;
  top: 0;
  height: 100vh;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 36px;
  padding: 0 8px;
}

.logo-icon { font-size: 28px; }
.logo-title { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 16px; color: #fff; }
.logo-sub { font-size: 11px; color: #555; text-transform: uppercase; letter-spacing: 1px; }

.sidebar-nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  border: none;
  background: none;
  color: #888;
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
}
.nav-item:hover { background: #1a1a2e; color: #ccc; }
.nav-item.active { background: linear-gradient(135deg, #667eea22, #764ba222); color: #a78bfa; font-weight: 500; }

.sidebar-footer { margin-top: auto; }

.admin-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: #1a1a2e;
  border-radius: 8px;
  margin-bottom: 10px;
  font-size: 13px;
}
.admin-name { font-weight: 500; color: #ddd; font-size: 13px; }
.admin-role { font-size: 11px; color: #666; }

.btn-voltar {
  width: 100%;
  padding: 8px;
  background: none;
  border: 1px solid #2a2a40;
  border-radius: 8px;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-voltar:hover { color: #aaa; border-color: #3a3a55; }

/* MAIN */
.main-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}
.page-header h1 {
  font-family: 'Syne', sans-serif;
  font-size: 28px;
  font-weight: 800;
  color: #fff;
}

.btn-refresh {
  padding: 8px 16px;
  background: #1a1a2e;
  border: 1px solid #2a2a40;
  border-radius: 8px;
  color: #888;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-refresh:hover { color: #a78bfa; border-color: #a78bfa44; }

/* CARDS */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #13131f;
  border: 1px solid #1e1e30;
  border-radius: 12px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
}
.stat-card.blue::before { background: linear-gradient(90deg, #667eea, #764ba2); }
.stat-card.purple::before { background: linear-gradient(90deg, #a78bfa, #7c3aed); }
.stat-card.red::before { background: linear-gradient(90deg, #f87171, #dc2626); }
.stat-card.green::before { background: linear-gradient(90deg, #34d399, #059669); }
.stat-card.orange::before { background: linear-gradient(90deg, #fb923c, #ea580c); }

.stat-icon { font-size: 24px; margin-bottom: 12px; }
.stat-value { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #fff; line-height: 1; }
.stat-label { font-size: 13px; color: #666; margin-top: 4px; }
.stat-sub { font-size: 12px; color: #4ade80; margin-top: 6px; }

/* SECTION CARD */
.section-card {
  background: #13131f;
  border: 1px solid #1e1e30;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}
.section-card h2 {
  font-family: 'Syne', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #ddd;
  margin-bottom: 20px;
}

/* BAR CHART */
.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  height: 140px;
  padding-top: 24px;
}
.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: flex-end;
  gap: 6px;
}
.bar-value { font-size: 12px; color: #888; }
.bar-fill {
  width: 100%;
  background: linear-gradient(180deg, #a78bfa, #667eea);
  border-radius: 4px 4px 0 0;
  transition: height 0.5s ease;
  min-height: 4px;
}
.bar-label { font-size: 11px; color: #555; }

/* PROGRESS */
.progress-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #888;
}
.progress-bar {
  flex: 1;
  height: 8px;
  background: #1e1e30;
  border-radius: 999px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.5s ease;
}
.green-fill { background: linear-gradient(90deg, #34d399, #059669); }
.gray-fill { background: #2a2a40; }

/* TABLE */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.data-table th {
  text-align: left;
  padding: 8px 12px;
  color: #555;
  font-weight: 500;
  border-bottom: 1px solid #1e1e30;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
}
.data-table td {
  padding: 12px;
  border-bottom: 1px solid #1a1a2a;
  color: #ccc;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: #1a1a2e; }
.muted { color: #666 !important; }

.tipo-badge {
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 500;
}
.tipo-badge.admin { background: #7c3aed22; color: #a78bfa; }
.tipo-badge.user { background: #0e4a2a; color: #4ade80; }

/* RANKING */
.rank-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #1a1a2a;
}
.rank-item:last-child { border-bottom: none; }
.rank-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #1e1e30;
  color: #666;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.rank-title { flex: 1; font-size: 14px; color: #ccc; }
.rank-count { font-size: 13px; color: #888; }

.two-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

/* ESTADOS */
.center-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
  color: #555;
}
.error-state { color: #f87171; }
.spinner {
  width: 40px; height: 40px;
  border: 3px solid #1e1e30;
  border-top-color: #a78bfa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty { color: #444; font-size: 13px; padding: 16px 0; }

.btn-primary {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .sidebar { display: none; }
  .two-cols { grid-template-columns: 1fr; }
}
</style>
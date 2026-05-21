<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
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
  if (!isLogged.value) { router.push('/login'); return }
  await fetchStats()
})

const fetchStats = async () => {
  loading.value = true; error.value = ''
  try {
    const { data } = await apiClient.get('/admin-stats/')
    stats.value = data
  } catch {
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
  <div class="d-flex" style="min-height:100vh;background:#0d0d14;color:#e8e6f0">

    <!-- Sidebar -->
    <aside class="d-flex flex-column p-3" style="width:240px;background:#13131f;border-right:1px solid #1e1e30;position:sticky;top:0;height:100vh">
      <div class="d-flex align-items-center gap-2 mb-4 px-2">
        <span style="font-size:28px">🎬</span>
        <div>
          <div class="fw-bold text-white" style="font-size:15px">MovieFlix</div>
          <div style="font-size:11px;color:#555;text-transform:uppercase;letter-spacing:1px">Painel Admin</div>
        </div>
      </div>

      <nav class="d-flex flex-column gap-1 flex-grow-1">
        <button
          v-for="tab in [{ id:'overview', label:'📊 Visão Geral' }, { id:'usuarios', label:'👥 Usuários' }, { id:'conteudo', label:'🎥 Conteúdo' }]"
          :key="tab.id"
          @click="activeTab = tab.id as any"
          class="btn text-start px-3 py-2 rounded-2 border-0 fw-medium"
          :style="{
            background: activeTab === tab.id ? 'linear-gradient(135deg,rgba(102,126,234,0.15),rgba(118,75,162,0.15))' : 'none',
            color: activeTab === tab.id ? '#a78bfa' : '#888',
            fontSize: '14px'
          }"
        >
          {{ tab.label }}
        </button>
      </nav>

      <div class="mt-auto">
        <div class="d-flex align-items-center gap-2 p-2 rounded-2 mb-2" style="background:#1a1a2e;font-size:13px">
          <span>⚙️</span>
          <div>
            <div class="fw-medium" style="color:#ddd">{{ user?.nome || user?.email }}</div>
            <div style="font-size:11px;color:#666">Administrador</div>
          </div>
        </div>
        <button @click="router.push('/')" class="btn w-100 py-1" style="border:1px solid #2a2a40;color:#666;font-size:13px;background:none">
          ← Voltar ao site
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-grow-1 p-4" style="overflow-y:auto">

      <!-- Loading -->
      <div v-if="loading" class="d-flex flex-column align-items-center justify-content-center" style="min-height:400px;gap:16px;color:#555">
        <div class="mf-spinner" style="border-top-color:#a78bfa"></div>
        <p>Carregando dados...</p>
      </div>

      <!-- Erro -->
      <div v-else-if="error" class="d-flex flex-column align-items-center justify-content-center gap-3" style="min-height:400px;color:#f87171">
        <div style="font-size:48px">⚠️</div>
        <p>{{ error }}</p>
        <button @click="fetchStats" class="btn px-4 py-2 fw-semibold" style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:8px">
          Tentar novamente
        </button>
      </div>

      <template v-else-if="stats">

        <!-- VISÃO GERAL -->
        <div v-if="activeTab === 'overview'">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="fw-bold text-white mb-0" style="font-size:26px">Visão Geral</h1>
            <button @click="fetchStats" class="btn btn-sm px-3" style="background:#1a1a2e;border:1px solid #2a2a40;color:#888;font-size:13px">↻ Atualizar</button>
          </div>

          <!-- Cards -->
          <div class="row row-cols-2 row-cols-lg-4 g-3 mb-4">
            <div class="col" v-for="card in [
              { color:'#667eea,#764ba2', icon:'👥', value: stats.usuarios.total, label:'Usuários', sub:`+${stats.usuarios.hoje} hoje` },
              { color:'#a78bfa,#7c3aed', icon:'💬', value: stats.comentarios.total, label:'Comentários', sub:`Nota média: ⭐ ${stats.comentarios.media_nota}/10` },
              { color:'#f87171,#dc2626', icon:'❤️', value: stats.favoritos.total, label:'Favoritos', sub:`+${stats.favoritos.ultimos_7_dias} esta semana` },
              { color:'#34d399,#059669', icon:'📋', value: stats.watchlist.total, label:'Watchlist', sub:`${taxaAssistidos}% assistidos` },
            ]" :key="card.label">
              <div class="p-3 rounded-3 position-relative overflow-hidden" style="background:#13131f;border:1px solid #1e1e30">
                <div class="position-absolute top-0 start-0 end-0" :style="{ height:'3px', background:`linear-gradient(90deg,${card.color})` }"></div>
                <div class="mb-2" style="font-size:22px">{{ card.icon }}</div>
                <div class="fw-bold text-white mb-1" style="font-size:28px">{{ card.value }}</div>
                <div style="font-size:13px;color:#666">{{ card.label }}</div>
                <div style="font-size:12px;color:#4ade80;margin-top:4px">{{ card.sub }}</div>
              </div>
            </div>
          </div>

          <!-- Gráfico cadastros -->
          <div class="p-4 rounded-3 mb-4" style="background:#13131f;border:1px solid #1e1e30">
            <h2 class="fw-bold mb-4" style="font-size:15px;color:#ddd">📈 Cadastros nos últimos 7 dias</h2>
            <div class="d-flex align-items-end gap-2" style="height:140px">
              <div v-for="dia in stats.usuarios.cadastros_por_dia" :key="dia.dia" class="d-flex flex-column align-items-center flex-grow-1" style="height:100%;justify-content:flex-end;gap:6px">
                <span style="font-size:12px;color:#888">{{ dia.total }}</span>
                <div :style="{ height:`${Math.max((dia.total/maxCadastros)*100,4)}%`, background:'linear-gradient(180deg,#a78bfa,#667eea)', borderRadius:'4px 4px 0 0', width:'100%', minHeight:'4px', transition:'height 0.5s' }"></div>
                <span style="font-size:11px;color:#555">{{ dia.dia }}</span>
              </div>
            </div>
          </div>

          <!-- Progress watchlist -->
          <div class="p-4 rounded-3" style="background:#13131f;border:1px solid #1e1e30">
            <h2 class="fw-bold mb-3" style="font-size:15px;color:#ddd">📋 Status da Watchlist</h2>
            <div v-for="row in [
              { label: `Assistidos (${stats.watchlist.assistidos})`, pct: taxaAssistidos, color: 'linear-gradient(90deg,#34d399,#059669)' },
              { label: `Pendentes (${stats.watchlist.pendentes})`, pct: 100-taxaAssistidos, color: '#2a2a40' },
            ]" :key="row.label" class="d-flex align-items-center gap-3 mb-2" style="font-size:13px;color:#888">
              <span style="min-width:160px">{{ row.label }}</span>
              <div class="flex-grow-1 rounded-pill overflow-hidden" style="height:8px;background:#1e1e30">
                <div :style="{ width:row.pct+'%', height:'100%', background:row.color, borderRadius:'999px', transition:'width 0.5s' }"></div>
              </div>
              <span>{{ row.pct }}%</span>
            </div>
          </div>
        </div>

        <!-- USUÁRIOS -->
        <div v-if="activeTab === 'usuarios'">
          <h1 class="fw-bold text-white mb-4" style="font-size:26px">Usuários</h1>
          <div class="row row-cols-2 row-cols-lg-4 g-3 mb-4">
            <div class="col" v-for="card in [
              { color:'#667eea,#764ba2', icon:'👥', value: stats.usuarios.total, label:'Total' },
              { color:'#a78bfa,#7c3aed', icon:'📅', value: stats.usuarios.ultimos_7_dias, label:'Últimos 7 dias' },
              { color:'#34d399,#059669', icon:'🟢', value: stats.usuarios.ativos_semana, label:'Ativos esta semana' },
              { color:'#fb923c,#ea580c', icon:'🗓️', value: stats.usuarios.ultimos_30_dias, label:'Últimos 30 dias' },
            ]" :key="card.label">
              <div class="p-3 rounded-3 position-relative overflow-hidden" style="background:#13131f;border:1px solid #1e1e30">
                <div class="position-absolute top-0 start-0 end-0" :style="{ height:'3px', background:`linear-gradient(90deg,${card.color})` }"></div>
                <div class="mb-2" style="font-size:22px">{{ card.icon }}</div>
                <div class="fw-bold text-white mb-1" style="font-size:28px">{{ card.value }}</div>
                <div style="font-size:13px;color:#666">{{ card.label }}</div>
              </div>
            </div>
          </div>

          <div class="p-4 rounded-3" style="background:#13131f;border:1px solid #1e1e30">
            <h2 class="fw-bold mb-3" style="font-size:15px;color:#ddd">👤 Usuários recentes</h2>
            <div class="table-responsive">
              <table class="table table-dark table-hover mb-0" style="font-size:13px;--bs-table-bg:#13131f;--bs-table-border-color:#1e1e30">
                <thead>
                  <tr style="color:#555;font-size:11px;text-transform:uppercase;letter-spacing:0.5px">
                    <th>#</th><th>Nome</th><th>Email</th><th>Tipo</th><th>Cadastro</th><th>Último login</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="u in stats.usuarios.recentes" :key="u.id">
                    <td style="color:#555">{{ u.id }}</td>
                    <td>{{ u.nome || '—' }}</td>
                    <td style="color:#555">{{ u.email }}</td>
                    <td>
                      <span class="badge rounded-pill px-2" :style="u.tipo_usuario==='admin' ? 'background:rgba(124,58,237,0.13);color:#a78bfa' : 'background:#0e4a2a;color:#4ade80'">
                        {{ u.tipo_usuario || 'user' }}
                      </span>
                    </td>
                    <td style="color:#555">{{ formatDate(u.data_criacao) }}</td>
                    <td style="color:#555">{{ formatDate(u.last_login) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- CONTEÚDO -->
        <div v-if="activeTab === 'conteudo'">
          <h1 class="fw-bold text-white mb-4" style="font-size:26px">Conteúdo</h1>

          <div class="row g-3 mb-4">
            <div class="col-12 col-md-6">
              <div class="p-4 rounded-3 h-100" style="background:#13131f;border:1px solid #1e1e30">
                <h2 class="fw-bold mb-3" style="font-size:15px;color:#ddd">❤️ Filmes mais favoritados</h2>
                <p v-if="stats.favoritos.top_filmes.length === 0" style="color:#444;font-size:13px">Nenhum dado ainda</p>
                <div v-for="(filme, i) in stats.favoritos.top_filmes" :key="filme.filme_id" class="d-flex align-items-center gap-3 py-2" style="border-bottom:1px solid #1a1a2a">
                  <span class="d-flex align-items-center justify-content-center rounded-circle fw-bold flex-shrink-0" style="width:24px;height:24px;background:#1e1e30;color:#666;font-size:12px">{{ Number(i)+1 }}</span>
                  <span class="flex-grow-1" style="font-size:14px;color:#ccc">{{ filme.titulo || `Filme #${filme.filme_id}` }}</span>
                  <span style="font-size:13px;color:#888">{{ filme.total }} ❤️</span>
                </div>
              </div>
            </div>
            <div class="col-12 col-md-6">
              <div class="p-4 rounded-3 h-100" style="background:#13131f;border:1px solid #1e1e30">
                <h2 class="fw-bold mb-3" style="font-size:15px;color:#ddd">💬 Filmes mais na watchlist</h2>
                <p v-if="stats.watchlist.top_filmes.length === 0" style="color:#444;font-size:13px">Nenhum dado ainda</p>
                <div v-for="(filme, i) in stats.watchlist.top_filmes" :key="filme.filme_id" class="d-flex align-items-center gap-3 py-2" style="border-bottom:1px solid #1a1a2a">
                  <span class="d-flex align-items-center justify-content-center rounded-circle fw-bold flex-shrink-0" style="width:24px;height:24px;background:#1e1e30;color:#666;font-size:12px">{{ Number(i)+1 }}</span>
                  <span class="flex-grow-1" style="font-size:14px;color:#ccc">{{ filme.titulo || `Filme #${filme.filme_id}` }}</span>
                  <span style="font-size:13px;color:#888">{{ filme.total }} 💬</span>
                </div>
              </div>
            </div>
          </div>

          <div class="p-4 rounded-3" style="background:#13131f;border:1px solid #1e1e30">
            <h2 class="fw-bold mb-3" style="font-size:15px;color:#ddd">💬 Comentários</h2>
            <div class="row row-cols-2 row-cols-lg-4 g-3">
              <div class="col" v-for="card in [
                { color:'#a78bfa,#7c3aed', icon:'💬', value: stats.comentarios.total, label:'Total' },
                { color:'#667eea,#764ba2', icon:'📅', value: stats.comentarios.hoje, label:'Hoje' },
                { color:'#34d399,#059669', icon:'⭐', value: stats.comentarios.media_nota, label:'Nota média /10' },
                { color:'#fb923c,#ea580c', icon:'📆', value: stats.comentarios.ultimos_7_dias, label:'Últimos 7 dias' },
              ]" :key="card.label">
                <div class="p-3 rounded-3 position-relative overflow-hidden" style="background:#0d0d14;border:1px solid #1e1e30">
                  <div class="position-absolute top-0 start-0 end-0" :style="{ height:'3px', background:`linear-gradient(90deg,${card.color})` }"></div>
                  <div class="mb-2" style="font-size:20px">{{ card.icon }}</div>
                  <div class="fw-bold text-white mb-1" style="font-size:24px">{{ card.value }}</div>
                  <div style="font-size:13px;color:#666">{{ card.label }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </template>
    </main>
  </div>
</template>

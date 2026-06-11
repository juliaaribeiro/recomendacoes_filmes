# 🎬 MovieFlix - Sistema de Recomendação de Filmes

Aplicação para descobrir, avaliar e organizar filmes usando Django REST Framework e Vue.js 3, com recomendações personalizadas geradas por IA.

## 🚀 Funcionalidades

### Visitantes (sem login)
- Ver filmes populares em tempo real
- Buscar filmes por nome
- Visualizar detalhes completos dos filmes
- Ver avaliações públicas de outros usuários

### Usuários logados
- Avaliar filmes com notas de 1 a 10 e comentar
- Adicionar e remover favoritos
- Criar e gerenciar watchlist pessoal
- Marcar filmes como assistidos
- **Receber recomendações personalizadas por IA** com base nos próprios favoritos, watchlist e avaliações

### Administradores
- Painel com estatísticas de usuários, comentários, favoritos e watchlist
- Visualização de ranking de filmes mais favoritados
- Gráfico de cadastros dos últimos 7 dias

## 🛠️ Stack Tecnológico

### Backend
- **Django 6.0** + **Django REST Framework** — API REST
- **JWT** — Autenticação segura
- **SQLite** (desenvolvimento) / **PostgreSQL** (produção)
- **django-grappelli** — Interface admin aprimorada
- **Google Gemini API** — Geração de recomendações por IA
- **Cache do Django** — Recomendações armazenadas por 30 minutos

### Frontend
- **Vue.js 3** + **TypeScript** — Framework e tipagem
- **Vite** — Build tool
- **Vue Router** — Roteamento
- **Axios** — HTTP Client
- **Bootstrap 5** — Framework CSS

### APIs Externas
- **The Movie Database (TMDB)** — Base de dados de filmes e posters
- **Google Gemini** — IA para recomendações personalizadas (gratuito)

## 📋 Pré-requisitos

- Python 3.12+
- Node.js 20+
- Chave de API do TMDB — gratuita em https://www.themoviedb.org/settings/api
- Chave de API do Gemini — gratuita em https://aistudio.google.com/apikey

## 🔧 Instalação e execução

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd recomendacoes_filmes
```

### 2. Backend

```bash
# Criar e ativar ambiente virtual
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves
```

Edite o arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-secret-key-django
TMDB_API_KEY=sua-chave-tmdb
GEMINI_API_KEY=sua-chave-gemini
```

```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

Servidor disponível em: **http://localhost:8000**

### 3. Frontend

```bash
cd frontend

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com sua chave do TMDB
```

Edite o arquivo `frontend/.env`:

```env
VITE_TMDB_API_KEY=sua-chave-tmdb
VITE_API_BASE_URL=http://localhost:8000
```

```bash
# Instalar dependências
npm install

# Rodar servidor de desenvolvimento
npm run dev
```

Servidor disponível em: **http://localhost:5173**

> ⚠️ O frontend possui seu próprio `.env`, separado do backend. Ambos os arquivos estão no `.gitignore` — use os `.env.example` como referência.

## 📁 Estrutura do Projeto

```
recomendacoes_filmes/
├── .env.example               # Variáveis de ambiente do backend (referência)
├── .env                       # Variáveis reais — NÃO sobe para o git
├── movie_recommendation/      # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                     # Autenticação e perfil de usuários
├── movies/                    # Integração com a API do TMDB
├── comments/                  # Comentários e avaliações
├── favorites/                 # Favoritos por usuário
├── watchlist/                 # Watchlist por usuário
├── recommendations/           # Recomendações personalizadas por IA
│   ├── views.py               # Consulta o banco + chama o Gemini
│   └── urls.py
├── frontend/                  # Vue.js Frontend
│   ├── .env.example           # Variáveis de ambiente do frontend (referência)
│   ├── .env                   # Variáveis reais — NÃO sobe para o git
│   └── src/
│       ├── assets/            # CSS global e utilitários Bootstrap
│       ├── components/        # Componentes reutilizáveis (MovieCard)
│       ├── composables/       # useAuth
│       ├── router/            # Configuração de rotas
│       ├── utils/             # axiosConfig, api
│       └── views/             # Páginas da aplicação
└── manage.py
```

## 🤖 Como funcionam as recomendações

1. O backend faz SELECT nos favoritos, watchlist e avaliações do usuário logado
2. Monta um perfil de gosto cinematográfico e envia para o **Gemini 2.5 Flash**
3. A IA retorna 5 filmes recomendados em JSON com título, ano, gênero e motivo personalizado
4. O frontend busca o poster de cada filme na API do TMDB e exibe os cards
5. O resultado fica em **cache por 30 minutos** — clicar em "Gerar novas recomendações" força uma nova chamada à IA

## 🔌 Endpoints da API

### Usuários
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/usuarios/cadastro/` | Criar conta |
| POST | `/usuarios/login/` | Fazer login |
| GET | `/usuarios/perfil/` | Obter perfil |
| PUT | `/usuarios/perfil/` | Atualizar perfil |

### Filmes
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/filmes/populares/` | Filmes populares |
| GET | `/filmes/busca/?q=nome` | Buscar filmes |
| GET | `/filmes/{id}/` | Detalhes do filme |

### Comentários e Avaliações
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/comentarios/` | Listar comentários |
| POST | `/comentarios/` | Criar comentário com nota (1–10) |
| PATCH | `/comentarios/{id}/` | Editar comentário |
| DELETE | `/comentarios/{id}/` | Excluir comentário |

### Favoritos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/favoritos/` | Listar favoritos |
| POST | `/favoritos/` | Adicionar favorito |
| DELETE | `/favoritos/{id}/` | Remover favorito |

### Watchlist
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/watchlist/` | Listar watchlist |
| POST | `/watchlist/` | Adicionar à watchlist |
| PATCH | `/watchlist/{id}/` | Atualizar status (assistido) |
| DELETE | `/watchlist/{id}/` | Remover da watchlist |

### Recomendações
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/recomendacoes/` | Recomendações personalizadas (cache 30 min) |
| GET | `/recomendacoes/?force=true` | Forçar nova geração pela IA |

### Admin
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/admin-stats/` | Estatísticas do painel admin |

## 📝 Rotas do Frontend

| Rota | View | Descrição |
|------|------|-----------|
| `/` | HomeView | Filmes populares |
| `/search` | SearchView | Busca de filmes |
| `/movie/:id` | MovieDetailView | Detalhes do filme |
| `/login` | LoginView | Login |
| `/register` | RegisterView | Cadastro |
| `/meus-favoritos` | FavoritesView | Favoritos do usuário |
| `/minha-watchlist` | WatchlistView | Watchlist do usuário |
| `/recomendacoes` | RecommendationsView | Recomendações por IA |
| `/admin-dashboard` | AdminDashboard | Painel administrativo |

## 🎨 Identidade Visual

Tema dark com paleta customizada sobre Bootstrap 5:

- Fundo: `#0F0F1B` com gradiente radial
- Cards: `#1A1A2E`
- Destaque principal: gradiente `#FF3CAC → #00C6FF`
- Destaque secundário: gradiente `#7B2FF7 → #00C6FF`
- Texto: `#E5E7EB`

## 🚀 Deploy

### Backend — Heroku
```bash
heroku create nome-do-app
heroku config:set SECRET_KEY=... TMDB_API_KEY=... GEMINI_API_KEY=...
git push heroku main
```

### Frontend — Vercel
```bash
npm run build
# Fazer deploy da pasta dist/ no Vercel
# Configurar as variáveis VITE_* no painel do Vercel
```

---

**Desenvolvido com ❤️ usando Django + Vue.js + Bootstrap 5 + Gemini AI**
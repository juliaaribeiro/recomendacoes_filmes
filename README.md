# 🎬 MovieFlix - Sistema de Recomendação de Filmes

Aplicação moderna para descobrir, avaliar e obter recomendações de filmes usando Django, PostgreSQL e Vue.js 3.

## 🚀 Funcionalidades

### Para Visitantes (Sem Login)
- ✅ Ver filmes populares em tempo real
- ✅ Buscar filmes por nome
- ✅ Visualizar detalhes completos dos filmes
- ✅ Ver avaliações públicas de outros usuários
- ✅ Sistema de autenticação (Login/Cadastro)

### Para Usuários Logados (Em desenvolvimento)
- Avaliar filmes (1-10 estrelas) e comentar
- Adicionar à lista de favoritos
- Criar watchlist pessoal
- Receber recomendações personalizadas
- Ver histórico de interações

## 🛠️ Stack Tecnológico

### Backend
- **Django 6.0** - Framework web
- **Django REST Framework** - API REST
- **JWT** - Autenticação segura
- **SQLite** (Dev) / PostgreSQL (Prod)
- **CORS** - Integração frontend-backend

### Frontend
- **Vue.js 3** - Framework JavaScript
- **TypeScript** - Tipagem estática
- **Vite** - Build tool ultrarrápido
- **Vue Router** - Roteamento
- **Axios** - HTTP Client
- **Tailwind CSS** - Estilização

### API Externa
- **The Movie Database (TMDB)** - Base de dados de filmes

## 📋 Pré-requisitos

- Python 3.9+
- Node.js 18+
- npm ou yarn
- Chave API do TMDB (gratuita em https://www.themoviedb.org/settings/api)

## 🔧 Instalação

### 1. Backend Setup

```bash
cd c:/Users/Júlia/Desktop/web

# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

Servidor roda em: **http://localhost:8000**

### 2. Frontend Setup

```bash
cd frontend

# Instalar dependências
npm install

# Rodar servidor de desenvolvimento
npm run dev
```

Servidor roda em: **http://localhost:5173**

## 📁 Estrutura do Projeto

```
web/
├── movie_recommendation/    # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                   # App de Usuários
│   ├── models.py
│   ├── views.py
│   ├── stats_views.py       # Dashboard de estatísticas (admin)
│   ├── serializers.py
│   └── urls.py
├── movies/                  # App de Filmes (TMDB API)
├── comments/                # App de Comentários
├── favorites/               # App de Favoritos
├── watchlist/               # App de Watchlist
├── frontend/                # Vue.js Frontend
│   ├── src/
│   │   ├── components/      # Componentes Vue
│   │   ├── views/           # Páginas
│   │   │   └── AdminDashboard.vue  # Painel administrativo
│   │   ├── router/          # Configuração de rotas
│   │   ├── composables/     # useAuth, useHoverStyle
│   │   └── utils/           # axiosConfig, api
│   └── package.json
└── manage.py
```

## 🔌 Endpoints da API

### Usuários
- `POST /usuarios/cadastro/` - Criar conta
- `POST /usuarios/login/` - Fazer login
- `GET /usuarios/perfil/` - Obter perfil (autenticado)
- `PUT /usuarios/perfil/` - Atualizar perfil (autenticado)

### Filmes
- `GET /filmes/populares/` - Filmes populares
- `GET /filmes/busca/?q=nome` - Buscar filmes
- `GET /filmes/{id}/` - Detalhes do filme
- `GET /filmes/trending/` - Filmes em tendência

### Avaliações (integradas aos comentários)
- `GET /comentarios/` - Meus comentários/avaliações
- `POST /comentarios/` - Criar comentário/avaliação (nota opcional 1-10)
- `PUT /comentarios/{id}/` - Atualizar comentário/avaliação
- `DELETE /comentarios/{id}/` - Deletar comentário/avaliação

### Favoritos (Autenticado)
- `GET /favoritos/` - Meus favoritos
- `POST /favoritos/` - Adicionar favorito
- `DELETE /favoritos/{id}/` - Remover favorito

### Watchlist (Autenticado)
- `GET /watchlist/` - Minha watchlist
- `POST /watchlist/` - Adicionar à watchlist
- `DELETE /watchlist/{id}/` - Remover da watchlist

### Admin (Autenticado como admin)
- `GET /admin-stats/` - Estatísticas do dashboard

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do backend:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
TMDB_API_KEY=sua-chave-tmdb
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📝 Rotas Frontend

| Rota | Componente | Descrição |
|------|-----------|-----------|
| `/` | HomeView | Home pública - Filmes populares |
| `/search` | SearchView | Buscar filmes |
| `/movie/:id` | MovieDetailView | Detalhes do filme |
| `/login` | LoginView | Página de login |
| `/register` | RegisterView | Página de cadastro |
| `/meus-favoritos` | FavoritesView | Lista de favoritos |
| `/minha-watchlist` | WatchlistView | Lista da watchlist |
| `/admin-dashboard` | AdminDashboard | Painel administrativo |

## 🎨 Paleta de Cores

- Primária: Azul (#2563EB)
- Secundária: Cinza (#6B7280)
- Sucesso: Verde (#10B981)
- Erro: Vermelho (#EF4444)
- Fundo: Claro (#F3F4F6)

## 🚀 Deploy

### Backend (Heroku)
```bash
heroku login
heroku create seu-app-name
git push heroku main
```

### Frontend (Vercel)
```bash
npm run build
# Fazer deploy de `dist/` folder no Vercel
```

## 🤝 Contribuições

Para contribuir:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT.

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Django + Vue.js**

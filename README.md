# Plataforma de Gestão de Pedidos — E-cCC

Plataforma interna de gestão de pedidos para e-commerce (E-Commerce Casa Cívil), construída com arquitetura de micro-frontends (Vue 3 + Module Federation) e microsserviços (FastAPI), comunicando-se via Nginx como API Gateway.

---

## Arquitetura

```mermaid
graph TD
    Client["Cliente (Browser)"]

    Client -->|":3000"| AppHost["app-host\nVue 3 Shell · Nginx :3000"]
    AppHost -->|"Module Federation"| MfeOrders["mfe-orders\nVue 3 Remote"]

    AppHost -->|"HTTP REST + JWT"| Nginx["Nginx API Gateway :8080"]
    MfeOrders -->|"HTTP REST + JWT"| Nginx

    Nginx -->|"/api/auth/*"| Auth["Auth Service :8001"]
    Nginx -->|"/api/orders/*"| Orders["Orders Service :8002"]

    Auth --> AuthDB[("auth_db <br> PostgreSQL :5433")]
    Auth --> Redis[("Redis <br> DB 0:6379/0 <br> DB 1:6379/1")]

    Orders --> OrdersDB[("orders_db <br> PostgreSQL :5434")]
    Orders --> Redis

    style AppHost   fill:#42b883,color:#fff,stroke:#33a06f
    style MfeOrders fill:#42b883,color:#fff,stroke:#33a06f
    style Redis     fill:#dc382c,color:#fff,stroke:#b71c1c,stroke-width:3px
    style Nginx     fill:#009639,color:#fff
    style Auth      fill:#2563eb,color:#fff
    style Orders    fill:#2563eb,color:#fff
```

### Componentes

| Componente | Tecnologia | Porta | Descrição |
|------------|-----------|-------|-----------|
| App Host | Vue 3 + Vite · Nginx | 3000 | Shell do frontend (Module Federation host) |
| MFE Orders | Vue 3 + Vite · Nginx | 3001 | Micro-frontend de pedidos (remote) |
| API Gateway | Nginx 1.25 | 8080 | Reverse proxy, roteamento por path |
| Auth Service | FastAPI + Python 3.12 | 8001 | Autenticação, gestão de usuários, JWT RS256 |
| Orders Service | FastAPI + Python 3.12 | 8002 | CRUD de pedidos, filtros por status |
| Auth DB | PostgreSQL 16 | 3000 | Banco exclusivo do serviço de auth |
| Orders DB | PostgreSQL 16 | 3001 | Banco exclusivo do serviço de pedidos |
| Redis DB 0 | Redis 7 | 6379/0 | Cache do Orders Service |
| Redis DB 1 | Redis 7 | 6379/1 | Cache do Auth Service |

---

## 🖥️ Frontend

A camada de apresentação é composta por dois aplicativos Vue 3 com **Module Federation (Vite)**:

### app-host — Shell da aplicação

- Vue 3 + Vuetify 3 + Vue Router
- Gerencia autenticação (login, registro, logout)
- Carrega o `mfe-orders` dinamicamente em runtime
- **Guarda de rota com verificação de expiração JWT**: decodifica o claim `exp` do token sem dependências externas e redireciona para `/login` se expirado

**Páginas:**

| Rota | Página | Descrição |
|------|--------|-----------|
| `/login` | LoginPage | Formulário de login |
| `/register` | RegisterPage | Registro de novo usuário |
| `/home` | HomePage | Dashboard do usuário autenticado |
| `/users` | UsersPage | Listagem de usuários com busca e filtro de status |
| `/orders` | OrdersList (MFE) | Listagem de pedidos (carregado via Module Federation) |
| `/orders/create` | OrderCreate (MFE) | Criação de pedido (carregado via Module Federation) |

### mfe-orders — Micro-frontend de pedidos

- Vue 3 exposto como remote via Module Federation
- Expõe `OrdersList` e `OrderCreate` para consumo pelo `app-host`

---

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados

### Subir a stack completa

```bash
docker compose up --build -d
```

### Verificar saúde dos serviços

```bash
curl http://localhost:8080/api/auth/health
curl http://localhost:8080/api/orders/health
```

### Acessar a aplicação

- **Frontend:** http://localhost:3000
- **Auth API Docs:** http://localhost:8080/api/auth/docs
- **Orders API Docs:** http://localhost:8080/api/orders/docs

---

## 📡 Endpoints da API

### Auth Service (`/api/auth`)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|-------------|
| POST | `/api/auth/register` | Registrar novo usuário | Não |
| POST | `/api/auth/login` | Login (retorna JWT) | Não |
| GET | `/api/auth/users` | Listar todos os usuários | JWT |
| GET | `/api/auth/users/me` | Dados do usuário logado | JWT |

### Orders Service (`/api/orders`)

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|-------------|
| GET | `/api/orders/` | Listar pedidos (filtro por status) | JWT |
| POST | `/api/orders/` | Criar pedido | JWT |
| GET | `/api/orders/{id}` | Consultar pedido por ID | JWT |
| PATCH | `/api/orders/{id}/status` | Atualizar status do pedido | JWT |

### Exemplo de uso

```bash
# 1. Registrar usuário
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@empresa.com","password":"senha123","full_name":"Admin"}'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@empresa.com","password":"senha123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 3. Criar pedido
curl -X POST http://localhost:8080/api/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "customer_name": "Cliente A",
    "items": [
      {"product_name": "Notebook Dell", "quantity": 1, "unit_price": 4500.00},
      {"product_name": "Mouse Logitech", "quantity": 2, "unit_price": 89.90}
    ]
  }'

# 4. Listar pedidos
curl http://localhost:8080/api/orders/ -H "Authorization: Bearer $TOKEN"

# 5. Atualizar status
curl -X PATCH http://localhost:8080/api/orders/{ORDER_ID}/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "confirmado"}'
```

---

## 🔧 Decisões Técnicas

### Por que FastAPI em vez de Django REST Framework?
- **Performance**: async nativo com `asyncpg`, sem overhead de synchronous ORM
- **Documentação automática**: Swagger/OpenAPI gerado automaticamente via Pydantic
- **Tipagem forte**: validators e serializers derivados dos type hints
- **Leveza**: ideal para microsserviços, sem o "batteries-included" do Django que seria desnecessário

### Por que SQLAlchemy 2.0 + asyncpg?
- ORM robusto com suporte a async sessions
- Migrações versionadas via Alembic
- Compatível com o padrão async do FastAPI sem adaptadores

### Por que Nginx como API Gateway?
- Reverse proxy leve e battle-tested
- Roteamento simples por path prefix (`/api/auth/`, `/api/orders/`)
- Facilmente extensível para load balancing, rate limiting, SSL termination

### Por que JWT RS256 (assimétrico)?
- **Stateless**: cada serviço valida o token com a chave pública sem chamada de rede
- **Segurança**: somente o Auth Service possui a chave privada para assinar tokens
- **Escalabilidade**: novos serviços só precisam da chave pública para validar

### Banco de dados separados (Database per Service)
- Isolamento total entre domínios
- Cada serviço é dono do seu schema
- Permite escolher tecnologias diferentes por serviço no futuro

### Cache com Redis (decorator pattern)

O cache é implementado via **decorators** na camada de rotas. A camada de serviço permanece inalterada.

```mermaid
sequenceDiagram
    participant Client
    participant Decorator as "@cached decorator"
    participant Handler as Route Handler
    participant Redis
    participant DB as PostgreSQL

    Client->>Decorator: GET /api/orders/{id}
    Decorator->>Redis: GET order:{id}
    alt Cache HIT
        Redis-->>Decorator: JSON armazenado
        Decorator-->>Client: JSONResponse (fast path)
    else Cache MISS
        Decorator->>Handler: chama handler original
        Handler->>DB: SELECT ...
        DB-->>Handler: resultado
        Handler-->>Decorator: Order ORM
        Decorator->>Redis: SET order:{id} (TTL)
        Decorator-->>Client: resposta normal
    end
```

| Decorator | Aplicado em | Função |
|---|---|---|
| `@cached(prefix, ttl)` | Endpoints `GET` | Cache-aside — chave gerada automaticamente a partir dos parâmetros da rota |
| `@invalidates_cache(*patterns)` | Endpoints `POST`, `PATCH` | Invalida chaves após escrita, suporta wildcards e interpolação |

| Variável | Default | Descrição |
|---|---|---|
| `CACHE_ENABLED` | `true` | Desativar cache sem remover o código |
| `CACHE_TTL_ORDER` | `600` | TTL em segundos para pedido individual |
| `CACHE_TTL_ORDER_LIST` | `300` | TTL em segundos para listagens |

> Se o Redis estiver indisponível, o app continua funcionando normalmente via PostgreSQL (graceful degradation).

### Guarda de expiração JWT (frontend)

O Vue Router decodifica o claim `exp` do JWT diretamente no `beforeEach` sem bibliotecas externas. Se o token estiver expirado, ele é removido do `localStorage` e o usuário é redirecionado para `/login`.

---

## 🧪 CI/CD

O repositório utiliza **GitHub Actions** com uma pipeline que executa os testes unitários de cada serviço **somente quando seu código muda** a cada push.

```yaml
# .github/workflows/tests.yml
jobs:
  changes:         # detecta quais serviços foram modificados
    uses: dorny/paths-filter@v4

  test-auth:       # roda apenas se services/auth/** mudou
    if: needs.changes.outputs.auth == 'true'

  test-orders:     # roda apenas se services/orders/** mudou
    if: needs.changes.outputs.orders == 'true'
```

- **Paths filter**: testes de um serviço não rodam quando apenas o outro muda
- Testes rodam com **SQLite em memória** — nenhum serviço externo necessário
- Chaves RSA do JWT são injetadas via **GitHub Secrets** (`JWT_PRIVATE_KEY`, `JWT_PUBLIC_KEY`)
- Cobertura atual: 15 testes (auth) + 33 testes (orders)

---

## 📋 O que ficaria diferente com mais tempo

### Implementaria
- **Alembic migrations** versionadas (atualmente tabelas são criadas pelo ORM no startup)
- **Comunicação assíncrona** entre serviços via Redis Pub/Sub ou RabbitMQ
- **Observabilidade** com logs estruturados (structlog), métricas (Prometheus) e tracing (OpenTelemetry)
- **Rate limiting** no Nginx
- **SSL/TLS** termination no gateway

### Decisões que não tomei e por quê
- **Não usei Django REST Framework**: seria overengineering para um PMV com microsserviços simples
- **Não implementei event sourcing**: complexidade desnecessária neste estágio; CRUD é suficiente para o domínio atual
- **Não separei em multi-repo**: a facilidade do mono-repo para Docker Compose e CI supera a independência de deploy neste PMV
- **Não usei API Gateway dedicado (Kong, Traefik)**: Nginx atende perfeitamente o caso de uso atual

---

## 🛑 Parar a stack

```bash
docker compose down

# Para remover também os volumes (dados):
docker compose down -v
```

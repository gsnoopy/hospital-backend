# BOBSIN - Hospital Backend API

API REST para sistema de Avaliações Técnicas desenvolvida com FastAPI, com autenticação JWT e banco PostgreSQL.

## 🚀 Tecnologias Utilizadas

### Backend Framework
- **FastAPI**: Framework web moderno e rápido para Python, com suporte nativo a documentação OpenAPI/Swagger e validação automática de dados
- **Uvicorn**: Servidor ASGI de alta performance para executar aplicações FastAPI

### Banco de Dados
- **PostgreSQL 17**: Banco de dados relacional robusto e escalável
- **SQLAlchemy**: ORM (Object-Relational Mapping) para Python, facilita interação com banco de dados
- **Alembic**: Ferramenta de migração de banco de dados para SQLAlchemy
- **psycopg2-binary**: Driver PostgreSQL para Python

### Autenticação e Segurança
- **PyJWT**: Biblioteca para criação e verificação de tokens JWT (JSON Web Tokens)
- **Bcrypt**: Algoritmo de hash seguro para criptografia de senhas
- **Pydantic**: Validação de dados e serialização com type hints
- **Role-Based Access Control**: Sistema de autorização baseado em roles

### Cache e Performance
- **Redis**: Cache em memória para sessões e rate limiting


### Containerização
- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração de múltiplos containers

### Configuração
- **pydantic-settings**: Gerenciamento de configurações e variáveis de ambiente

## 📁 Estrutura do Projeto

```
app/
├── auth/              # Módulo de autenticação
│   └── auth.py        # Lógica de autenticação
├── core/              # Configurações centrais
│   ├── config.py      # Settings da aplicação
│   ├── database.py    # Conexão com banco
│   └── timezone.py    # Configurações de fuso horário
├── decorators/        # Decorators para autenticação e autorização
│   ├── auth.py        # Decorators de autenticação JWT
│   └── roles.py       # Decorators de autorização por roles
├── middleware/        # Middlewares da aplicação
│   ├── error_handler.py  # Tratamento global de erros
│   └── rate_limit.py     # Middleware de rate limiting
├── models/           # Modelos SQLAlchemy
│   ├── user.py       # Modelo de usuário
│   └── role.py       # Modelo de roles
├── repositories/     # Camada de acesso a dados
│   ├── user_repository.py  # Repository de usuários
│   └── role_repository.py  # Repository de roles
├── routes/           # Endpoints da API
│   ├── auth_routes.py    # Rotas de autenticação
│   ├── user_routes.py    # Rotas de usuários
│   ├── role_routes.py    # Rotas de roles
│   └── health_routes.py  # Health check
├── schemas/          # Schemas Pydantic
│   ├── auth.py       # Schemas de autenticação
│   ├── user.py       # Schemas de usuário
│   ├── role.py       # Schemas de roles
│   ├── rate_limit.py # Schemas de rate limiting
│   └── pagination.py # Schemas de paginação
├── security/         # Utilitários de segurança
│   └── rate_limiter.py   # Rate limiter com Redis
├── services/         # Lógica de negócio
│   ├── auth_service.py   # Serviços de autenticação
│   ├── user_service.py   # Serviços de usuário
│   └── role_service.py   # Serviços de roles
├── utils/            # Utilitários gerais
│   └── exceptions.py # Exceções customizadas
├── validators/       # Validações de negócio
│   ├── base_validator.py  # Validador base
│   └── user_validator.py  # Validações de usuário
└── main.py          # Ponto de entrada da aplicação
```

## ⚙️ Pré-requisitos

- Docker e Docker Compose instalados
- PostgreSQL em Cloud

## 🏃‍♂️ Como Executar

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd bobsin-hospital-backend
```

### 2. Configure as variáveis de ambiente
Crie um arquivo `.env` baseado no template:
```env
DATABASE_URL=postgresql://user:password@host:port/database
TEST_DATABASE_URL=postgresql://user:password@host:port/test_database
ENVIRONMENT=development  # ou production
JWT_SECRET_KEY=sua_chave_secreta_jwt_aqui
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://redis:6379
```

### 3. Execute a aplicação
```bash
docker-compose up -d
```

### 4. Execute as migrações do banco
```bash
docker-compose exec app alembic upgrade head
```

## 📊 Serviços Disponíveis

Após executar `docker-compose up -d`, os seguintes serviços estarão disponíveis:

- **API**: http://localhost:8000
  - Documentação Swagger: http://localhost:8000/docs
  - Documentação ReDoc: http://localhost:8000/redoc
  - Health Check: http://localhost:8000/health
- **Redis**: localhost:6379

## 🔧 Comandos Úteis

### Logs da aplicação
```bash
docker-compose logs -f app
```

### Executar migrações
```bash
docker-compose exec app alembic upgrade head
```

### Criar nova migração
```bash
docker-compose exec app alembic revision --autogenerate -m "descrição"
```

### Parar todos os serviços
```bash
docker-compose down
```

### Rebuild da aplicação
```bash
docker-compose up --build
```

## 🎯 Funcionalidades

- **Autenticação JWT**: Login/logout com tokens seguros
- **Sistema de Roles**: Controle de acesso baseado em perfis (admin, user, etc.)
- **Rate Limiting**: Proteção contra abuso de API
- **Health Check**: Endpoint para monitoramento de saúde da aplicação
- **Migrações**: Controle de versão do banco de dados com Alembic

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DATABASE_URL` | URL do banco PostgreSQL (produção) | `postgresql://user:pass@host/db` |
| `TEST_DATABASE_URL` | URL do banco PostgreSQL (desenvolvimento) | `postgresql://user:pass@host/testdb` |
| `ENVIRONMENT` | Ambiente da aplicação | `development` ou `production` |
| `JWT_SECRET_KEY` | Chave secreta para JWT | `sua_chave_super_secreta` |
| `JWT_ALGORITHM` | Algoritmo de assinatura JWT | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token | `30` |
| `REDIS_URL` | URL do Redis | `redis://redis:6379` |


## 🏗️ Arquitetura

O projeto segue os princípios SOLID com arquitetura em camadas:
- **Routes**: Definição de endpoints
- **Services**: Lógica de negócio
- **Repositories**: Acesso aos dados
- **Models**: Representação das tabelas
- **Schemas**: Validação de entrada/saída
- **Validators**: Regras de negócio específicas

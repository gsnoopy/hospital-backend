from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.role_routes import router as role_router
from app.routes.hospital_routes import router as hospital_router
from app.routes.job_title_routes import router as job_title_router
from app.routes.health_routes import router as health_router
from app.routes.category_routes import router as category_router
from app.routes.subcategory_routes import router as subcategory_router
from app.routes.catalog_routes import router as catalog_router
from app.core.database import engine, Base
from app.security import rate_limiter
from app.core.config import settings
from app.middleware.error_handler import error_handler_middleware
from app.middleware.rate_limit import rate_limit_middleware

# [DATABASE INITIALIZATION]
# [Cria todas as tabelas do banco de dados baseadas nos modelos SQLAlchemy]
# [ENTRADA: engine - engine de conexão com o banco]
# [SAIDA: None - cria tabelas no banco]
# [DEPENDENCIAS: Base.metadata, engine]
Base.metadata.create_all(bind=engine)

# [RATE LIMITER INITIALIZATION]
# [Inicializa o rate limiter com conexão Redis]
# [ENTRADA: settings.redis_url - URL de conexão do Redis]
# [SAIDA: None - configura rate limiter global]
# [DEPENDENCIAS: rate_limiter, settings]
rate_limiter.initialize(settings.redis_url)

# [FASTAPI APPLICATION]
# [Cria instância principal da aplicação FastAPI com metadados]
# [ENTRADA: configurações de title, description, version]
# [SAIDA: FastAPI - instância da aplicação web]
# [DEPENDENCIAS: FastAPI]
app = FastAPI(
    title="Hospital Backend API",
    description="FastAPI backend with JWT authentication and PostgreSQL",
    version="1.0.0"
)

# [CORS MIDDLEWARE]
# [Adiciona middleware CORS para permitir requisições cross-origin]
# [ENTRADA: allow_origins - lista de origens permitidas]
# [SAIDA: None - configura CORS na aplicação]
# [DEPENDENCIAS: app, CORSMiddleware]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [ERROR HANDLER MIDDLEWARE]
# [Adiciona middleware global para tratamento de erros HTTP]
# [ENTRADA: error_handler_middleware - função middleware]
# [SAIDA: None - registra middleware na aplicação]
# [DEPENDENCIAS: app, error_handler_middleware]
app.middleware("http")(error_handler_middleware)

# [RATE LIMIT MIDDLEWARE]
# [Adiciona middleware global para rate limiting HTTP]
# [ENTRADA: rate_limit_middleware - função middleware]
# [SAIDA: None - registra middleware na aplicação]
# [DEPENDENCIAS: app, rate_limit_middleware]
app.middleware("http")(rate_limit_middleware)


# [ROUTER REGISTRATION]
# [Registra todos os routers da aplicação com seus endpoints]
# [ENTRADA: routers - auth, user, role, enterprise, job_title, vacation, leave_type, leave, hospital, health]
# [SAIDA: None - adiciona rotas à aplicação]
# [DEPENDENCIAS: app, todos os routers importados]
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(hospital_router)
app.include_router(job_title_router)
app.include_router(health_router)
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(catalog_router)

# [READ ROOT]
# [Endpoint GET raiz que retorna mensagem de status da API]
# [ENTRADA: nenhuma]
# [SAIDA: dict - mensagem indicando que API está rodando]
# [DEPENDENCIAS: app]
@app.get("/")
def read_root():
    return {"message": "3DI RH Backend API is running!"}
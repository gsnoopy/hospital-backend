from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# [DATABASE ENGINE]
# [Cria o engine do SQLAlchemy configurado com timezone para conectar ao banco de dados]
# [ENTRADA: settings.get_database_url() - URL de conexão do banco]
# [SAIDA: Engine - instância do engine SQLAlchemy configurado]
# [DEPENDENCIAS: create_engine, settings.get_database_url]
engine = create_engine(
    settings.get_database_url(),
    connect_args={
        "options": "-c timezone=America/Sao_Paulo"
    }
)
# [SESSION FACTORY]
# [Cria factory de sessões SQLAlchemy configurada para não fazer autocommit e autoflush]
# [ENTRADA: engine - engine de conexão com banco]
# [SAIDA: SessionLocal - classe para criar sessões de banco]
# [DEPENDENCIAS: sessionmaker, engine]
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# [BASE MODEL]
# [Cria a classe base para todos os modelos SQLAlchemy usando declarative_base]
# [ENTRADA: nenhuma]
# [SAIDA: Base - classe base para herança dos modelos]
# [DEPENDENCIAS: declarative_base]
Base = declarative_base()


# [GET DATABASE SESSION]
# [Dependency injection function que fornece sessão de banco com cleanup automático]
# [ENTRADA: nenhuma]
# [SAIDA: Generator[Session] - sessão de banco que é fechada automaticamente]
# [DEPENDENCIAS: SessionLocal]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
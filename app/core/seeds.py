from datetime import datetime
from sqlalchemy import text
import bcrypt
from app.core.config import settings
from uuid_utils import uuid7


# [ADD DEFAULT DATA]
# [Adiciona dados padrão necessários para funcionamento da aplicação quando tabelas são criadas]
# [ENTRADA: connection - conexão ativa com banco de dados]
# [SAIDA: None - insere role, hospital, job_title e usuário desenvolvedor padrão]
# [DEPENDENCIAS: datetime, text, bcrypt, settings, uuid7]
def add_default_data(connection):

    try:
        connection.execute(text("SELECT 1 FROM roles LIMIT 1"))
        connection.execute(text("SELECT 1 FROM hospitals LIMIT 1"))
        connection.execute(text("SELECT 1 FROM job_titles LIMIT 1"))
        connection.execute(text("SELECT 1 FROM users LIMIT 1"))
    except Exception:
        print("Tabelas ainda não existem, pulando inserção de dados padrão...")
        return

    dev_email = settings.dev_email
    dev_password = settings.dev_password

    now = datetime.now()

    try:
        result = connection.execute(text("SELECT COUNT(*) FROM roles WHERE name = 'Desenvolvedor'")).scalar()
        if result == 0:
            print("Criando role Desenvolvedor...")
            connection.execute(text("""
                INSERT INTO roles (name, description, public_id, created_at, updated_at)
                VALUES ('Desenvolvedor', 'Acesso total ao sistema', :public_id, :now1, :now2)
            """), {"public_id": str(uuid7()), "now1": now, "now2": now})
    except Exception as e:
        print(f"Erro ao criar role: {e}")
        return

    try:
        result = connection.execute(text("SELECT COUNT(*) FROM hospitals WHERE name = 'Hospital Padrão'")).scalar()
        if result == 0:
            print("Criando hospital padrão...")
            connection.execute(text("""
                INSERT INTO hospitals (name, nationality, document_type, document, email, phone, city, public_id, created_at, updated_at)
                VALUES ('Hospital Padrão', 'Brasileira', 'CNPJ', '00.000.000/0001-00', 'contato@hospitalpadrao.com', '(11) 99999-9999', 'São Paulo', :public_id, :now1, :now2)
            """), {"public_id": str(uuid7()), "now1": now, "now2": now})
    except Exception as e:
        print(f"Erro ao criar hospital: {e}")
        return

    try:
        result = connection.execute(text("SELECT COUNT(*) FROM job_titles WHERE title = 'Desenvolvedor Full Stack'")).scalar()
        if result == 0:
            print("Criando cargo padrão...")
            connection.execute(text("""
                INSERT INTO job_titles (title, public_id, created_at, updated_at)
                VALUES ('Desenvolvedor Full Stack', :public_id, :now1, :now2)
            """), {"public_id": str(uuid7()), "now1": now, "now2": now})
    except Exception as e:
        print(f"Erro ao criar cargo: {e}")
        return

    role_id = connection.execute(text("SELECT id FROM roles WHERE name = 'Desenvolvedor'")).scalar()
    hospital_id = connection.execute(text("SELECT id FROM hospitals WHERE name = 'Hospital Padrão'")).scalar()
    job_title_id = connection.execute(text("SELECT id FROM job_titles WHERE title = 'Desenvolvedor Full Stack'")).scalar()

    try:
        result = connection.execute(text("SELECT COUNT(*) FROM users WHERE email = :email"), {"email": dev_email}).scalar()
        if result > 0:
            print(f"Usuário desenvolvedor já existe ({dev_email})!")
            return
    except Exception as e:
        print(f"Erro ao verificar usuário: {e}")
        return

    try:
        password_hash = bcrypt.hashpw(dev_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        print("Criando usuário desenvolvedor...")
        connection.execute(text("""
            INSERT INTO users (name, email, password, phone, role_id, job_title_id, hospital_id, is_active, public_id, created_at, updated_at)
            VALUES ('Desenvolvedor', :email, :password, '(11) 99999-9999', :role_id, :job_title_id, :hospital_id, TRUE, :public_id, :now1, :now2)
        """), {
            "email": dev_email,
            "password": password_hash,
            "role_id": role_id,
            "job_title_id": job_title_id,
            "hospital_id": hospital_id,
            "public_id": str(uuid7()),
            "now1": now,
            "now2": now
        })

    except Exception as e:
        print(f"Erro ao criar usuário desenvolvedor: {e}")
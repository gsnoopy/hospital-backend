from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional
from uuid import UUID

# [USER REPOSITORY]
# [Repository para operações CRUD da entidade User no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância UserRepository configurada]
# [DEPENDENCIAS: Session]
class UserRepository:
    
    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE USER]
    # [Cria um novo usuário no banco com senha hasheada e carrega todos os relacionamentos]
    # [ENTRADA: user_data - dados do usuário via schema, hashed_password - senha já hasheada, role_internal_id - ID interno da role, job_title_internal_id - ID interno do cargo, hospital_internal_id - ID interno do hospital]
    # [SAIDA: User - instância do usuário criado com relacionamentos carregados]
    # [DEPENDENCIAS: User, self.db, joinedload]
    def create(self, user_data: UserCreate, hashed_password: str, role_internal_id: int, job_title_internal_id: Optional[int] = None, hospital_internal_id: Optional[int] = None) -> User:
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password,
            phone=user_data.phone,
            role_id=role_internal_id,
            job_title_id=job_title_internal_id,
            hospital_id=hospital_internal_id,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        # Load all relationships
        db_user = self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.id == db_user.id).first()
        return db_user

    # [GET USER BY ID]
    # [Busca um usuário pelo seu ID interno com todos os relacionamentos carregados]
    # [ENTRADA: user_id - ID interno do usuário a ser buscado]
    # [SAIDA: Optional[User] - usuário com relacionamentos ou None se não existir]
    # [DEPENDENCIAS: self.db, User, joinedload]
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.id == user_id).first()
    
    # [GET USER BY PUBLIC ID]
    # [Busca um usuário pelo seu UUID público com todos os relacionamentos carregados]
    # [ENTRADA: public_id - UUID público do usuário a ser buscado]
    # [SAIDA: Optional[User] - usuário com relacionamentos ou None se não existir]
    # [DEPENDENCIAS: self.db, User, joinedload, UUID]
    def get_by_public_id(self, public_id: UUID) -> Optional[User]:
        return self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.public_id == public_id).first()

    # [GET USER BY EMAIL]
    # [Busca um usuário pelo seu email único com todos os relacionamentos carregados]
    # [ENTRADA: email - email do usuário a ser buscado]
    # [SAIDA: Optional[User] - usuário encontrado ou None se não existir]
    # [DEPENDENCIAS: self.db, User, joinedload]
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.email == email).first()

    # [GET USER BY PHONE]
    # [Busca um usuário pelo telefone único]
    # [ENTRADA: phone - telefone do usuário a ser buscado]
    # [SAIDA: Optional[User] - usuário encontrado ou None se não existir]
    # [DEPENDENCIAS: self.db, User]
    def get_by_phone(self, phone: str) -> Optional[User]:
        return self.db.query(User).filter(User.phone == phone).first()


    # [GET USERS BY ROLE ID]
    # [Busca usuários por role com paginação]
    # [ENTRADA: role_id - ID interno da role, skip - registros a pular, limit - limite]
    # [SAIDA: list[User] - lista de usuários da role]
    # [DEPENDENCIAS: self.db, User, joinedload]
    def get_by_role_id(self, role_id: int, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.role_id == role_id).offset(skip).limit(limit).all()

    # [GET USERS BY JOB TITLE ID]
    # [Busca usuários por cargo com paginação]
    # [ENTRADA: job_title_id - ID interno do cargo, skip - registros a pular, limit - limite]
    # [SAIDA: list[User] - lista de usuários do cargo]
    # [DEPENDENCIAS: self.db, User, joinedload]
    def get_by_job_title_id(self, job_title_id: int, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.job_title_id == job_title_id).offset(skip).limit(limit).all()

    # [GET USERS BY HOSPITAL ID]
    # [Busca usuários por hospital com paginação]
    # [ENTRADA: hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: list[User] - lista de usuários do hospital]
    # [DEPENDENCIAS: self.db, User, joinedload]
    def get_by_hospital_id(self, hospital_id: int, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.hospital_id == hospital_id).offset(skip).limit(limit).all()

    # [GET ALL USERS]
    # [Busca todos os usuários com paginação e todos os relacionamentos carregados]
    # [ENTRADA: skip - número de registros a pular, limit - limite de registros]
    # [SAIDA: list[User] - lista de usuários com relacionamentos]
    # [DEPENDENCIAS: self.db, User, joinedload]
    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).offset(skip).limit(limit).all()
    
    # [GET TOTAL COUNT]
    # [Conta o total de usuários no banco de dados]
    # [ENTRADA: nenhuma]
    # [SAIDA: int - número total de usuários]
    # [DEPENDENCIAS: self.db, User]
    def get_total_count(self) -> int:
        return self.db.query(User).count()

    # [UPDATE USER]
    # [Atualiza um usuário existente no banco de dados]
    # [ENTRADA: user - instância do usuário, user_data - dados de atualização, role_internal_id - ID interno da role, job_title_internal_id - ID interno do cargo, hospital_internal_id - ID interno do hospital]
    # [SAIDA: User - usuário atualizado com dados atuais do banco]
    # [DEPENDENCIAS: self.db, joinedload]
    def update(self, user: User, user_data: UserUpdate, role_internal_id: Optional[int] = None, job_title_internal_id: Optional[int] = None, hospital_internal_id: Optional[int] = None) -> User:
        update_data = user_data.model_dump(exclude_unset=True, exclude={'role_id', 'job_title_id', 'hospital_id'})
        for field, value in update_data.items():
            setattr(user, field, value)
        
        # Update foreign key relationships if provided
        if role_internal_id is not None:
            user.role_id = role_internal_id
        if job_title_internal_id is not None:
            user.job_title_id = job_title_internal_id
        if hospital_internal_id is not None:
            user.hospital_id = hospital_internal_id
        
        self.db.commit()
        self.db.refresh(user)
        # Load all relationships
        user = self.db.query(User).options(
            joinedload(User.role),
            joinedload(User.job_title),
            joinedload(User.hospital)
        ).filter(User.id == user.id).first()
        return user

    # [DELETE USER]
    # [Remove um usuário do banco de dados]
    # [ENTRADA: user - instância do usuário a ser removido]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
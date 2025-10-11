from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.job_title_repository import JobTitleRepository
from app.repositories.hospital_repository import HospitalRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.auth import hash_password
from app.validators.user_validator import UserValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [USER SERVICE]
# [Serviço para gestão de usuários com validações, hash de senha e relacionamentos]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância UserService configurada]
# [DEPENDENCIAS: UserRepository, UserValidator]
class UserService:
    
    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de usuário]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: UserRepository, RoleRepository, JobTitleRepository, HospitalRepository, UserValidator]
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)
        self.job_title_repository = JobTitleRepository(db)
        self.hospital_repository = HospitalRepository(db)
        self.user_validator = UserValidator()

    # [CREATE USER]
    # [Cria novo usuário com validação, verificação de duplicatas, hash de senha e relacionamentos]
    # [ENTRADA: user_data - dados do usuário via UserCreate]
    # [SAIDA: User - usuário criado ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.user_validator, self.user_repository, hash_password]
    def create_user(self, user_data: UserCreate) -> User:
        validation_result = self.user_validator.validate(user_data)
        if not validation_result.is_valid:
            errors = validation_result.get_errors_by_field()
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(f"{field}: {msg}")

            raise HTTPException(
                status_code=422,
                detail={
                    "error": True,
                    "message": f"Validation error: {'; '.join(error_messages)}",
                    "status_code": 422
                }
            )

        # Check for unique constraints
        if self.user_repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"User with email '{user_data.email}' already exists",
                    "status_code": 409
                }
            )

        if self.user_repository.get_by_document(user_data.document):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"User with document '{user_data.document}' already exists",
                    "status_code": 409
                }
            )

        if self.user_repository.get_by_phone(user_data.phone):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"User with phone '{user_data.phone}' already exists",
                    "status_code": 409
                }
            )

        # Resolve foreign key relationships
        role = self.role_repository.get_by_public_id(user_data.role_id)
        if not role:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Role with ID '{user_data.role_id}' not found",
                    "status_code": 404
                }
            )

        job_title_internal_id = None
        if user_data.job_title_id:
            job_title = self.job_title_repository.get_by_public_id(user_data.job_title_id)
            if not job_title:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"JobTitle with ID '{user_data.job_title_id}' not found",
                        "status_code": 404
                    }
                )
            job_title_internal_id = job_title.id

        hospital_internal_id = None
        if user_data.hospital_id:
            hospital = self.hospital_repository.get_by_public_id(user_data.hospital_id)
            if not hospital:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"Hospital with ID '{user_data.hospital_id}' not found",
                        "status_code": 404
                    }
                )
            hospital_internal_id = hospital.id

        hashed_password = hash_password(user_data.password)
        user = self.user_repository.create(
            user_data,
            hashed_password,
            role.id,
            job_title_internal_id,
            hospital_internal_id
        )

        return user

    # [GET USER BY PUBLIC ID]
    # [Busca um usuário pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do usuário]
    # [SAIDA: Optional[User] - usuário encontrado ou None]
    # [DEPENDENCIAS: self.user_repository]
    def get_user_by_public_id(self, public_id: UUID) -> Optional[User]:
        return self.user_repository.get_by_public_id(public_id)

    # [GET USER BY EMAIL]
    # [Busca um usuário pelo seu email]
    # [ENTRADA: email - email do usuário]
    # [SAIDA: Optional[User] - usuário encontrado ou None]
    # [DEPENDENCIAS: self.user_repository]
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)

    # [GET USER BY DOCUMENT]
    # [Busca um usuário pelo documento]
    # [ENTRADA: document - documento do usuário]
    # [SAIDA: Optional[User] - usuário encontrado ou None]
    # [DEPENDENCIAS: self.user_repository]
    def get_user_by_document(self, document: str) -> Optional[User]:
        return self.user_repository.get_by_document(document)

    # [GET USERS BY NATIONALITY]
    # [Busca usuários por nacionalidade com paginação]
    # [ENTRADA: nationality - nacionalidade, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[User] - usuários paginados da nacionalidade]
    # [DEPENDENCIAS: self.user_repository, PaginatedResponse]
    def get_users_by_nationality(self, nationality: str, pagination: PaginationParams) -> PaginatedResponse[User]:
        users = self.user_repository.get_by_nationality(
            nationality=nationality,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.user_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=users,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET USERS BY ROLE]
    # [Busca usuários por role com paginação usando UUID público]
    # [ENTRADA: role_public_id - UUID público da role, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[User] - usuários paginados da role]
    # [DEPENDENCIAS: self.user_repository, self.role_repository, PaginatedResponse]
    def get_users_by_role(self, role_public_id: UUID, pagination: PaginationParams) -> PaginatedResponse[User]:
        role = self.role_repository.get_by_public_id(role_public_id)
        if not role:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Role with ID '{role_public_id}' not found",
                    "status_code": 404
                }
            )
        
        users = self.user_repository.get_by_role_id(
            role_id=role.id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.user_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=users,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET USERS BY JOB TITLE]
    # [Busca usuários por cargo com paginação usando UUID público]
    # [ENTRADA: job_title_public_id - UUID público do cargo, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[User] - usuários paginados do cargo]
    # [DEPENDENCIAS: self.user_repository, self.job_title_repository, PaginatedResponse]
    def get_users_by_job_title(self, job_title_public_id: UUID, pagination: PaginationParams) -> PaginatedResponse[User]:
        job_title = self.job_title_repository.get_by_public_id(job_title_public_id)
        if not job_title:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"JobTitle with ID '{job_title_public_id}' not found",
                    "status_code": 404
                }
            )
        
        users = self.user_repository.get_by_job_title_id(
            job_title_id=job_title.id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.user_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=users,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET USERS BY HOSPITAL]
    # [Busca usuários por hospital com paginação usando UUID público]
    # [ENTRADA: hospital_public_id - UUID público do hospital, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[User] - usuários paginados do hospital]
    # [DEPENDENCIAS: self.user_repository, self.hospital_repository, PaginatedResponse]
    def get_users_by_hospital(self, hospital_public_id: UUID, pagination: PaginationParams) -> PaginatedResponse[User]:
        hospital = self.hospital_repository.get_by_public_id(hospital_public_id)
        if not hospital:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Hospital with ID '{hospital_public_id}' not found",
                    "status_code": 404
                }
            )
        
        users = self.user_repository.get_by_hospital_id(
            hospital_id=hospital.id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.user_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=users,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET PAGINATED USERS]
    # [Busca usuários com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[User] - usuários paginados com metadados]
    # [DEPENDENCIAS: self.user_repository, PaginatedResponse]
    def get_paginated_users(self, pagination: PaginationParams) -> PaginatedResponse[User]:
        users = self.user_repository.get_all(
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.user_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=users,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE USER]
    # [Atualiza um usuário existente]
    # [ENTRADA: public_id - UUID público do usuário, user_data - dados de atualização]
    # [SAIDA: Optional[User] - usuário atualizado ou None se não encontrado]
    # [DEPENDENCIAS: self.user_repository]
    def update_user(self, public_id: UUID, user_data: UserUpdate) -> Optional[User]:
        user = self.user_repository.get_by_public_id(public_id)
        if not user:
            return None
        
        # Check for conflicts if fields are being updated
        if user_data.email and user_data.email != user.email:
            existing_user = self.user_repository.get_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"User with email '{user_data.email}' already exists",
                        "status_code": 409
                    }
                )

        if user_data.document and user_data.document != user.document:
            existing_user = self.user_repository.get_by_document(user_data.document)
            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"User with document '{user_data.document}' already exists",
                        "status_code": 409
                    }
                )

        if user_data.phone and user_data.phone != user.phone:
            existing_user = self.user_repository.get_by_phone(user_data.phone)
            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"User with phone '{user_data.phone}' already exists",
                        "status_code": 409
                    }
                )

        # Resolve foreign key relationships
        role_internal_id = None
        if user_data.role_id:
            role = self.role_repository.get_by_public_id(user_data.role_id)
            if not role:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"Role with ID '{user_data.role_id}' not found",
                        "status_code": 404
                    }
                )
            role_internal_id = role.id

        job_title_internal_id = None
        if user_data.job_title_id:
            job_title = self.job_title_repository.get_by_public_id(user_data.job_title_id)
            if not job_title:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"JobTitle with ID '{user_data.job_title_id}' not found",
                        "status_code": 404
                    }
                )
            job_title_internal_id = job_title.id

        hospital_internal_id = None
        if user_data.hospital_id:
            hospital = self.hospital_repository.get_by_public_id(user_data.hospital_id)
            if not hospital:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"Hospital with ID '{user_data.hospital_id}' not found",
                        "status_code": 404
                    }
                )
            hospital_internal_id = hospital.id
        
        return self.user_repository.update(
            user, 
            user_data, 
            role_internal_id,
            job_title_internal_id,
            hospital_internal_id
        )

    # [DELETE USER]
    # [Remove um usuário do sistema]
    # [ENTRADA: public_id - UUID público do usuário a ser removido]
    # [SAIDA: bool - True se removido, False se não encontrado]
    # [DEPENDENCIAS: self.user_repository]
    def delete_user(self, public_id: UUID) -> bool:
        user = self.user_repository.get_by_public_id(public_id)
        if not user:
            return False
        
        self.user_repository.delete(user)
        return True
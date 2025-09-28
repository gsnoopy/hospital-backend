from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_auth, require_roles
from app.models.user import User
from uuid import UUID

# [USER ROUTER]
# [Router FastAPI para endpoints CRUD de usuários com prefixo /users]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de usuários]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/users", tags=["users"])


# [CREATE USER]
# [Endpoint POST para criar um novo usuário - endpoint público para registro]
# [ENTRADA: user_data - dados do usuário via UserCreate, db - sessão do banco]
# [SAIDA: UserResponse - usuário criado (status 201) ou HTTPException 422 com erros de validação]
# [DEPENDENCIAS: UserService, ValidationException, HTTPException, status]
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    return user_service.create_user(user_data)


# [GET USERS]
# [Endpoint GET para listar usuários com paginação - requer autenticação]
# [ENTRADA: page - número da página (min 1), size - itens por página (1-25), db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários]
# [DEPENDENCIAS: PaginationParams, UserService, require_auth]
@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_paginated_users(pagination)


# [GET CURRENT USER PROFILE]
# [Endpoint GET para obter perfil do usuário atualmente autenticado]
# [ENTRADA: current_user - usuário autenticado via require_auth]
# [SAIDA: UserResponse - dados do usuário atual]
# [DEPENDENCIAS: require_auth]
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(require_auth)):
    return current_user


# [GET USER]
# [Endpoint GET para buscar um usuário pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público do usuário, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: UserResponse - dados do usuário ou HTTPException 404 se não encontrado]
# [DEPENDENCIAS: UserService, HTTPException, require_auth]
@router.get("/{public_id}", response_model=UserResponse)
def get_user(
    public_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    user_service = UserService(db)
    user = user_service.get_user_by_public_id(public_id)

    if not user:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("User", public_id)

    return user




# [GET USERS BY NATIONALITY]
# [Endpoint GET para buscar usuários por nacionalidade - requer autenticação]
# [ENTRADA: nationality - nacionalidade dos usuários, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários da nacionalidade]
# [DEPENDENCIAS: UserService, PaginationParams, require_auth]
@router.get("/nationality/{nationality}", response_model=PaginatedResponse[UserResponse])
def get_users_by_nationality(
    nationality: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_users_by_nationality(nationality, pagination)


# [GET USERS BY ROLE]
# [Endpoint GET para buscar usuários por role - requer autenticação]
# [ENTRADA: role_public_id - UUID público da role, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários da role]
# [DEPENDENCIAS: UserService, PaginationParams, require_auth]
@router.get("/role/{role_public_id}", response_model=PaginatedResponse[UserResponse])
def get_users_by_role(
    role_public_id: UUID,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_users_by_role(role_public_id, pagination)


# [GET USERS BY JOB TITLE]
# [Endpoint GET para buscar usuários por cargo - requer autenticação]
# [ENTRADA: job_title_public_id - UUID público do cargo, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários do cargo]
# [DEPENDENCIAS: UserService, PaginationParams, require_auth]
@router.get("/job-title/{job_title_public_id}", response_model=PaginatedResponse[UserResponse])
def get_users_by_job_title(
    job_title_public_id: UUID,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_users_by_job_title(job_title_public_id, pagination)


# [GET USERS BY HOSPITAL]
# [Endpoint GET para buscar usuários por hospital - requer autenticação]
# [ENTRADA: hospital_public_id - UUID público do hospital, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários do hospital]
# [DEPENDENCIAS: UserService, PaginationParams, require_auth]
@router.get("/hospital/{hospital_public_id}", response_model=PaginatedResponse[UserResponse])
def get_users_by_hospital(
    hospital_public_id: UUID,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_users_by_hospital(hospital_public_id, pagination)


# [UPDATE USER]
# [Endpoint PUT para atualizar um usuário - requer autenticação]
# [ENTRADA: public_id - UUID público do usuário, user_data - dados de atualização, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: UserResponse - usuário atualizado ou HTTPException 404]
# [DEPENDENCIAS: UserService, HTTPException, require_auth]
@router.put("/{public_id}", response_model=UserResponse)
def update_user(
    public_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    user_service = UserService(db)
    user = user_service.update_user(public_id, user_data)

    if not user:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("User", public_id)

    return user


# [DELETE USER]
# [Endpoint DELETE para remover um usuário - requer autenticação]
# [ENTRADA: public_id - UUID público do usuário, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: dict - mensagem de sucesso ou HTTPException 404]
# [DEPENDENCIAS: UserService, HTTPException, require_auth]
@router.delete("/{public_id}")
def delete_user(
    public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    user_service = UserService(db)
    success = user_service.delete_user(public_id)

    if not success:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("User", public_id)

    return {"message": "User deleted successfully"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.hospital_context import HospitalContext
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_auth, require_role
from app.models.user import User
from uuid import UUID

# [USER ROUTER]
# [Router FastAPI para endpoints CRUD de usuários com prefixo /users]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de usuários]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/users", tags=["users"])


# [CREATE USER]
# [Endpoint POST para criar um novo usuário - requer Desenvolvedor ou Administrador]
# [ENTRADA: user_data - dados do usuário, context - contexto de hospital, db - sessão do banco]
# [SAIDA: UserResponse - usuário criado (status 201) ou HTTPException 422 com erros de validação]
# [DEPENDENCIAS: UserService, require_role_and_hospital, HospitalContext]
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    # Validar o role que está sendo criado
    from app.repositories.role_repository import RoleRepository
    role_repo = RoleRepository(db)
    role_to_create = role_repo.get_by_public_id(user_data.role_id)

    if not role_to_create:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    # Se não for Desenvolvedor, aplicar restrições
    if not context.is_developer:
        # Administrador NÃO pode criar Desenvolvedor
        if role_to_create.name == "Desenvolvedor":
            raise HTTPException(
                status_code=403,
                detail="Only Desenvolvedor can create users with Desenvolvedor role"
            )

        # Força usar o hospital do usuário autenticado
        from app.repositories.hospital_repository import HospitalRepository
        hospital_repo = HospitalRepository(db)
        hospital = hospital_repo.get_by_id(context.hospital_id)
        if hospital:
            user_data.hospital_id = hospital.public_id

    user_service = UserService(db)
    return user_service.create_user(user_data)


# [GET USERS]
# [Endpoint GET para listar usuários - Desenvolvedor vê todos, Administrador vê apenas do próprio hospital]
# [ENTRADA: page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários]
# [DEPENDENCIAS: PaginationParams, UserService, require_role_and_hospital, HospitalContext]
@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_paginated_users(pagination, context.hospital_id)


# [GET CURRENT USER PROFILE]
# [Endpoint GET para obter perfil do usuário atualmente autenticado]
# [ENTRADA: current_user - usuário autenticado via require_auth]
# [SAIDA: UserResponse - dados do usuário atual]
# [DEPENDENCIAS: require_auth]
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(require_auth)):
    return current_user


# [GET USER]
# [Endpoint GET para buscar um usuário pelo UUID público - requer Desenvolvedor ou Administrador]
# [ENTRADA: public_id - UUID público do usuário, context - contexto de hospital, db - sessão do banco]
# [SAIDA: UserResponse - dados do usuário ou HTTPException 404]
# [DEPENDENCIAS: UserService, require_role_and_hospital, HospitalContext]
@router.get("/{public_id}", response_model=UserResponse)
def get_user(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = user_service.get_user_by_public_id(public_id)

    if not user:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("User", public_id)

    # Valida se pode acessar o usuário
    if not context.is_developer and user.hospital_id != context.hospital_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view users from your own hospital"
        )

    return user




# [GET USERS BY ROLE]
# [Endpoint GET para buscar usuários por role - requer Desenvolvedor ou Administrador]
# [ENTRADA: role_public_id - UUID público da role, page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários da role]
# [DEPENDENCIAS: UserService, PaginationParams, require_role_and_hospital, HospitalContext]
@router.get("/role/{role_public_id}", response_model=PaginatedResponse[UserResponse])
def get_users_by_role(
    role_public_id: UUID,
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_users_by_role(role_public_id, pagination, context.hospital_id)


# [GET USERS BY JOB TITLE]
# [Endpoint GET para buscar usuários por cargo - requer Desenvolvedor ou Administrador]
# [ENTRADA: job_title_public_id - UUID público do cargo, page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários do cargo]
# [DEPENDENCIAS: UserService, PaginationParams, require_role_and_hospital, HospitalContext]
@router.get("/job-title/{job_title_public_id}", response_model=PaginatedResponse[UserResponse])
def get_users_by_job_title(
    job_title_public_id: UUID,
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_users_by_job_title(job_title_public_id, pagination, context.hospital_id)


# [GET USERS BY HOSPITAL]
# [Endpoint GET para buscar usuários por hospital - requer Desenvolvedor ou Administrador]
# [ENTRADA: hospital_public_id - UUID público do hospital, page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[UserResponse] - lista paginada de usuários do hospital]
# [DEPENDENCIAS: UserService, PaginationParams, require_role_and_hospital, HospitalContext]
@router.get("/hospital/{hospital_public_id}", response_model=PaginatedResponse[UserResponse])
def get_users_by_hospital(
    hospital_public_id: UUID,
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    from app.repositories.hospital_repository import HospitalRepository
    hospital_repo = HospitalRepository(db)
    requested_hospital = hospital_repo.get_by_public_id(hospital_public_id)

    if requested_hospital:
        context.validate_hospital_access(requested_hospital.id)

    pagination = PaginationParams(page=page, size=size)
    user_service = UserService(db)
    return user_service.get_users_by_hospital(hospital_public_id, pagination)


# [UPDATE USER]
# [Endpoint PUT para atualizar um usuário - requer Desenvolvedor ou Administrador]
# [ENTRADA: public_id - UUID público do usuário, user_data - dados de atualização, context - contexto de hospital, db - sessão do banco]
# [SAIDA: UserResponse - usuário atualizado ou HTTPException 404]
# [DEPENDENCIAS: UserService, require_role_and_hospital, HospitalContext]
@router.put("/{public_id}", response_model=UserResponse)
def update_user(
    public_id: UUID,
    user_data: UserUpdate,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)

    # Busca o usuário antes de atualizar
    user = user_service.get_user_by_public_id(public_id)
    if not user:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("User", public_id)

    # Se não for Desenvolvedor, aplicar restrições
    if not context.is_developer:
        # Valida se o usuário pertence ao mesmo hospital
        if user.hospital_id != context.hospital_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update users from your own hospital"
            )

        # Administrador NÃO pode alterar hospital_id
        if user_data.hospital_id is not None:
            raise HTTPException(
                status_code=403,
                detail="Only Desenvolvedor can change hospital_id"
            )

        # Administrador NÃO pode atribuir role "Desenvolvedor"
        if user_data.role_id is not None:
            from app.repositories.role_repository import RoleRepository
            role_repo = RoleRepository(db)
            new_role = role_repo.get_by_public_id(user_data.role_id)

            if new_role and new_role.name == "Desenvolvedor":
                raise HTTPException(
                    status_code=403,
                    detail="Only Desenvolvedor can assign Desenvolvedor role"
                )

    # Atualiza o usuário
    updated_user = user_service.update_user(public_id, user_data)
    return updated_user


# [DELETE USER]
# [Endpoint DELETE para remover um usuário - requer Desenvolvedor ou Administrador]
# [ENTRADA: public_id - UUID público do usuário, context - contexto de hospital, db - sessão do banco]
# [SAIDA: dict - mensagem de sucesso ou HTTPException 404]
# [DEPENDENCIAS: UserService, require_role_and_hospital, HospitalContext]
@router.delete("/{public_id}")
def delete_user(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Desenvolvedor", "Administrador"])),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)

    # Busca o usuário antes de deletar
    user = user_service.get_user_by_public_id(public_id)
    if not user:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("User", public_id)

    # Valida se pode deletar o usuário
    if not context.is_developer and user.hospital_id != context.hospital_id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete users from your own hospital"
        )

    # Deleta o usuário
    success = user_service.delete_user(public_id)
    return {"message": "User deleted successfully"}

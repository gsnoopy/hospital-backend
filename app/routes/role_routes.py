from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.role_service import RoleService
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_auth, require_roles
from app.models.user import User
from uuid import UUID

# [ROLE ROUTER]
# [Router FastAPI para endpoints CRUD de roles com prefixo /roles]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de roles]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/roles", tags=["roles"])


# [CREATE ROLE]
# [Endpoint POST para criar uma nova role - restrito a desenvolvedores]
# [ENTRADA: role - dados da role via RoleCreate, db - sessão do banco, _ - usuário autenticado com role Desenvolvedor]
# [SAIDA: RoleResponse - role criada ou HTTPException 400 se já existe]
# [DEPENDENCIAS: RoleService, UserAlreadyExistsException, HTTPException, require_roles]
@router.post("/", response_model=RoleResponse)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("Desenvolvedor"))
):
    role_service = RoleService(db)
    return role_service.create_role(role)


# [GET ROLES]
# [Endpoint GET para listar roles com paginação - requer autenticação]
# [ENTRADA: page - número da página (min 1), size - itens por página (1-25), db - sessão do banco, _ - usuário autenticado]
# [SAIDA: PaginatedResponse[RoleResponse] - lista paginada de roles]
# [DEPENDENCIAS: PaginationParams, RoleService, require_auth]
@router.get("/", response_model=PaginatedResponse[RoleResponse])
def get_roles(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    _: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    role_service = RoleService(db)
    return role_service.get_paginated_roles(pagination)


# [GET ROLE]
# [Endpoint GET para buscar uma role pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público da role, db - sessão do banco, _ - usuário autenticado]
# [SAIDA: RoleResponse - dados da role ou HTTPException 404 se não encontrada]
# [DEPENDENCIAS: RoleService, HTTPException, require_auth]
@router.get("/{public_id}", response_model=RoleResponse)
def get_role(
    public_id: UUID, 
    db: Session = Depends(get_db),
    _: User = Depends(require_auth)
):
    role_service = RoleService(db)
    role = role_service.get_role_by_public_id(public_id)
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return role


# [UPDATE ROLE]
# [Endpoint PUT para atualizar uma role pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público da role, role_data - novos dados via RoleCreate, db - sessão do banco, _ - usuário autenticado]
# [SAIDA: RoleResponse - role atualizada ou HTTPException 404/400]
# [DEPENDENCIAS: RoleService, UserAlreadyExistsException, HTTPException, require_auth]
@router.put("/{public_id}", response_model=RoleResponse)
def update_role(
    public_id: UUID,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_auth)
):
    role_service = RoleService(db)
    role = role_service.update_role(public_id, role_data)
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return role


# [DELETE ROLE]
# [Endpoint DELETE para remover uma role pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público da role, db - sessão do banco, _ - usuário autenticado]
# [SAIDA: dict - mensagem de sucesso ou HTTPException 404 se não encontrada]
# [DEPENDENCIAS: RoleService, HTTPException, require_auth]
@router.delete("/{public_id}")
def delete_role(
    public_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_auth)
):
    role_service = RoleService(db)
    role = role_service.get_role_by_public_id(public_id)
    
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    role_service.delete_role(role)
    return {"message": "Role deleted successfully"}
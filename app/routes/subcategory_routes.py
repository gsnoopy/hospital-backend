from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.hospital_context import HospitalContext
from app.services.subcategory_service import SubCategoryService
from app.schemas.subcategory import SubCategoryCreate, SubCategoryUpdate, SubCategoryResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_role
from uuid import UUID


# [SUBCATEGORY ROUTER]
# [Router FastAPI para endpoints CRUD de subcategorias com prefixo /subcategories]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de subcategorias]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/subcategories", tags=["subcategories"])


# [CREATE SUBCATEGORY]
# [Endpoint POST para criar uma nova subcategoria - requer Desenvolvedor, Administrador ou Gerente]
# [ENTRADA: subcategory_data - dados da subcategoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: SubCategoryResponse - subcategoria criada (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: SubCategoryService, require_role_and_hospital, HospitalContext]
@router.post("/", response_model=SubCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    subcategory_data: SubCategoryCreate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    subcategory_service = SubCategoryService(db)
    return subcategory_service.create_subcategory(subcategory_data, context.hospital_id)


# [GET SUBCATEGORIES]
# [Endpoint GET para listar subcategorias - Desenvolvedor vê todas, outros veem apenas do próprio hospital]
# [ENTRADA: page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[SubCategoryResponse] - lista paginada de subcategorias]
# [DEPENDENCIAS: PaginationParams, SubCategoryService, require_role_and_hospital, HospitalContext]
@router.get("/", response_model=PaginatedResponse[SubCategoryResponse])
def get_subcategories(
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    subcategory_service = SubCategoryService(db)
    return subcategory_service.get_paginated_subcategories(pagination, context.hospital_id)


# [GET SUBCATEGORY]
# [Endpoint GET para buscar uma subcategoria pelo UUID público]
# [ENTRADA: public_id - UUID público da subcategoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: SubCategoryResponse - dados da subcategoria ou exceção]
# [DEPENDENCIAS: SubCategoryService, require_role_and_hospital, HospitalContext]
@router.get("/{public_id}", response_model=SubCategoryResponse)
def get_subcategory(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    subcategory_service = SubCategoryService(db)
    return subcategory_service.get_subcategory_by_public_id(public_id, context.hospital_id)


# [GET SUBCATEGORY BY NAME]
# [Endpoint GET para buscar uma subcategoria pelo nome]
# [ENTRADA: name - nome da subcategoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: SubCategoryResponse - dados da subcategoria ou 404]
# [DEPENDENCIAS: SubCategoryService, require_role_and_hospital, HospitalContext]
@router.get("/name/{name}", response_model=SubCategoryResponse)
def get_subcategory_by_name(
    name: str,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    subcategory_service = SubCategoryService(db)
    subcategory = subcategory_service.get_subcategory_by_name(name, context.hospital_id)

    if not subcategory:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("SubCategory", name)

    return subcategory


# [GET SUBCATEGORIES BY CATEGORY]
# [Endpoint GET para buscar subcategorias por categoria]
# [ENTRADA: category_id - UUID público da categoria, page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[SubCategoryResponse] - lista paginada de subcategorias da categoria]
# [DEPENDENCIAS: SubCategoryService, PaginationParams, require_role_and_hospital, HospitalContext]
@router.get("/category/{category_id}", response_model=PaginatedResponse[SubCategoryResponse])
def get_subcategories_by_category(
    category_id: UUID,
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    subcategory_service = SubCategoryService(db)
    return subcategory_service.get_subcategories_by_category(category_id, pagination, context.hospital_id)


# [UPDATE SUBCATEGORY]
# [Endpoint PUT para atualizar uma subcategoria]
# [ENTRADA: public_id - UUID público da subcategoria, subcategory_data - dados de atualização, context - contexto de hospital, db - sessão do banco]
# [SAIDA: SubCategoryResponse - subcategoria atualizada ou exceção]
# [DEPENDENCIAS: SubCategoryService, require_role_and_hospital, HospitalContext]
@router.put("/{public_id}", response_model=SubCategoryResponse)
def update_subcategory(
    public_id: UUID,
    subcategory_data: SubCategoryUpdate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    subcategory_service = SubCategoryService(db)
    return subcategory_service.update_subcategory(public_id, subcategory_data, context.hospital_id)


# [DELETE SUBCATEGORY]
# [Endpoint DELETE para remover uma subcategoria]
# [ENTRADA: public_id - UUID público da subcategoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: dict - mensagem de sucesso ou exceção]
# [DEPENDENCIAS: SubCategoryService, require_role_and_hospital, HospitalContext]
@router.delete("/{public_id}")
def delete_subcategory(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    subcategory_service = SubCategoryService(db)
    subcategory_service.delete_subcategory(public_id, context.hospital_id)
    return {"message": "SubCategory deleted successfully"}

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.hospital_context import HospitalContext
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithSubcategoriesResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_role
from uuid import UUID


# [CATEGORY ROUTER]
# [Router FastAPI para endpoints CRUD de categorias com prefixo /categories]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de categorias]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/categories", tags=["categories"])


# [CREATE CATEGORY]
# [Endpoint POST para criar uma nova categoria - requer Desenvolvedor, Administrador ou Gerente]
# [ENTRADA: category_data - dados da categoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: CategoryResponse - categoria criada (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: CategoryService, require_role_and_hospital, HospitalContext]
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    return category_service.create_category(category_data, context.hospital_id)


# [GET CATEGORIES]
# [Endpoint GET para listar categorias - Desenvolvedor vê todas, outros veem apenas do próprio hospital]
# [ENTRADA: page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[CategoryResponse] - lista paginada de categorias]
# [DEPENDENCIAS: PaginationParams, CategoryService, require_role_and_hospital, HospitalContext]
@router.get("/", response_model=PaginatedResponse[CategoryResponse])
def get_categories(
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    category_service = CategoryService(db)
    return category_service.get_paginated_categories(pagination, context.hospital_id)


# [GET CATEGORIES WITH SUBCATEGORIES]
# [Endpoint GET para listar categorias com subcategorias aninhadas]
# [ENTRADA: page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[CategoryWithSubcategoriesResponse] - lista paginada de categorias com subcategorias]
# [DEPENDENCIAS: PaginationParams, CategoryService, require_role_and_hospital, HospitalContext]
@router.get("/with-subcategories", response_model=PaginatedResponse[CategoryWithSubcategoriesResponse])
def get_categories_with_subcategories(
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    category_service = CategoryService(db)
    return category_service.get_paginated_categories_with_subcategories(pagination, context.hospital_id)


# [GET CATEGORY]
# [Endpoint GET para buscar uma categoria pelo UUID público]
# [ENTRADA: public_id - UUID público da categoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: CategoryResponse - dados da categoria ou exceção]
# [DEPENDENCIAS: CategoryService, require_role_and_hospital, HospitalContext]
@router.get("/{public_id}", response_model=CategoryResponse)
def get_category(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    return category_service.get_category_by_public_id(public_id, context.hospital_id)


# [GET CATEGORY BY NAME]
# [Endpoint GET para buscar uma categoria pelo nome]
# [ENTRADA: name - nome da categoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: CategoryResponse - dados da categoria ou 404]
# [DEPENDENCIAS: CategoryService, require_role_and_hospital, HospitalContext]
@router.get("/name/{name}", response_model=CategoryResponse)
def get_category_by_name(
    name: str,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    category = category_service.get_category_by_name(name, context.hospital_id)

    if not category:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("Category", name)

    return category


# [UPDATE CATEGORY]
# [Endpoint PUT para atualizar uma categoria]
# [ENTRADA: public_id - UUID público da categoria, category_data - dados de atualização, context - contexto de hospital, db - sessão do banco]
# [SAIDA: CategoryResponse - categoria atualizada ou exceção]
# [DEPENDENCIAS: CategoryService, require_role_and_hospital, HospitalContext]
@router.put("/{public_id}", response_model=CategoryResponse)
def update_category(
    public_id: UUID,
    category_data: CategoryUpdate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    return category_service.update_category(public_id, category_data, context.hospital_id)


# [DELETE CATEGORY]
# [Endpoint DELETE para remover uma categoria]
# [ENTRADA: public_id - UUID público da categoria, context - contexto de hospital, db - sessão do banco]
# [SAIDA: dict - mensagem de sucesso ou exceção]
# [DEPENDENCIAS: CategoryService, require_role_and_hospital, HospitalContext]
@router.delete("/{public_id}")
def delete_category(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    category_service.delete_category(public_id, context.hospital_id)
    return {"message": "Category deleted successfully"}

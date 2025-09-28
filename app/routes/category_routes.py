from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_auth
from app.models.user import User
from uuid import UUID


# [CATEGORY ROUTER]
# [Router FastAPI para endpoints CRUD de categorias com prefixo /categories]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de categorias]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/categories", tags=["categories"])


# [CREATE CATEGORY]
# [Endpoint POST para criar uma nova categoria - requer autenticação]
# [ENTRADA: category_data - dados da categoria via CategoryCreate, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CategoryResponse - categoria criada (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: CategoryService, require_auth]
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    category_service = CategoryService(db)
    return category_service.create_category(category_data)


# [GET CATEGORIES]
# [Endpoint GET para listar categorias com paginação - requer autenticação]
# [ENTRADA: page - número da página (min 1), size - itens por página (1-25), db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[CategoryResponse] - lista paginada de categorias]
# [DEPENDENCIAS: PaginationParams, CategoryService, require_auth]
@router.get("/", response_model=PaginatedResponse[CategoryResponse])
def get_categories(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    category_service = CategoryService(db)
    return category_service.get_paginated_categories(pagination)


# [GET CATEGORY]
# [Endpoint GET para buscar uma categoria pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público da categoria, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CategoryResponse - dados da categoria ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: CategoryService, require_auth]
@router.get("/{public_id}", response_model=CategoryResponse)
def get_category(
    public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    category_service = CategoryService(db)
    return category_service.get_category_by_public_id(public_id)


# [GET CATEGORY BY NAME]
# [Endpoint GET para buscar uma categoria pelo nome - requer autenticação]
# [ENTRADA: name - nome da categoria, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CategoryResponse - dados da categoria ou 404 se não encontrada]
# [DEPENDENCIAS: CategoryService, require_auth]
@router.get("/name/{name}", response_model=CategoryResponse)
def get_category_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    category_service = CategoryService(db)
    category = category_service.get_category_by_name(name)

    if not category:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("Category", name)

    return category


# [UPDATE CATEGORY]
# [Endpoint PUT para atualizar uma categoria - requer autenticação]
# [ENTRADA: public_id - UUID público da categoria, category_data - dados de atualização, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CategoryResponse - categoria atualizada ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: CategoryService, require_auth]
@router.put("/{public_id}", response_model=CategoryResponse)
def update_category(
    public_id: UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    category_service = CategoryService(db)
    return category_service.update_category(public_id, category_data)


# [DELETE CATEGORY]
# [Endpoint DELETE para remover uma categoria - requer autenticação]
# [ENTRADA: public_id - UUID público da categoria, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: dict - mensagem de sucesso ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: CategoryService, require_auth]
@router.delete("/{public_id}")
def delete_category(
    public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    category_service = CategoryService(db)
    category_service.delete_category(public_id)
    return {"message": "Category deleted successfully"}
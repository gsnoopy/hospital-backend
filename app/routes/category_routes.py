from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_hospital
from uuid import UUID


# [CATEGORY ROUTER]
# [Router FastAPI para endpoints CRUD de categorias com prefixo /categories]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de categorias]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/categories", tags=["categories"])


# [CREATE CATEGORY]
# [Endpoint POST para criar uma nova categoria - requer autenticação e extrai hospital do usuário]
# [ENTRADA: category_data - dados da categoria, hospital_id - ID do hospital (automático), db - sessão do banco]
# [SAIDA: CategoryResponse - categoria criada (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: CategoryService, require_hospital]
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    return category_service.create_category(category_data, hospital_id)


# [GET CATEGORIES]
# [Endpoint GET para listar categorias do hospital do usuário com paginação]
# [ENTRADA: page - número da página, size - itens por página, hospital_id - ID do hospital (automático), db - sessão do banco]
# [SAIDA: PaginatedResponse[CategoryResponse] - lista paginada de categorias do hospital]
# [DEPENDENCIAS: PaginationParams, CategoryService, require_hospital]
@router.get("/", response_model=PaginatedResponse[CategoryResponse])
def get_categories(
    page: int = 1,
    size: int = 10,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    category_service = CategoryService(db)
    return category_service.get_paginated_categories(pagination, hospital_id)


# [GET CATEGORY]
# [Endpoint GET para buscar uma categoria pelo UUID público (apenas do hospital do usuário)]
# [ENTRADA: public_id - UUID público da categoria, hospital_id - ID do hospital (automático), db - sessão do banco]
# [SAIDA: CategoryResponse - dados da categoria ou exceção]
# [DEPENDENCIAS: CategoryService, require_hospital]
@router.get("/{public_id}", response_model=CategoryResponse)
def get_category(
    public_id: UUID,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    return category_service.get_category_by_public_id(public_id, hospital_id)


# [GET CATEGORY BY NAME]
# [Endpoint GET para buscar uma categoria pelo nome (apenas do hospital do usuário)]
# [ENTRADA: name - nome da categoria, hospital_id - ID do hospital (automático), db - sessão do banco]
# [SAIDA: CategoryResponse - dados da categoria ou 404]
# [DEPENDENCIAS: CategoryService, require_hospital]
@router.get("/name/{name}", response_model=CategoryResponse)
def get_category_by_name(
    name: str,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    category = category_service.get_category_by_name(name, hospital_id)

    if not category:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("Category", name)

    return category


# [UPDATE CATEGORY]
# [Endpoint PUT para atualizar uma categoria (apenas do hospital do usuário)]
# [ENTRADA: public_id - UUID público da categoria, category_data - dados de atualização, hospital_id - ID do hospital (automático), db - sessão do banco]
# [SAIDA: CategoryResponse - categoria atualizada ou exceção]
# [DEPENDENCIAS: CategoryService, require_hospital]
@router.put("/{public_id}", response_model=CategoryResponse)
def update_category(
    public_id: UUID,
    category_data: CategoryUpdate,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    return category_service.update_category(public_id, category_data, hospital_id)


# [DELETE CATEGORY]
# [Endpoint DELETE para remover uma categoria (apenas do hospital do usuário)]
# [ENTRADA: public_id - UUID público da categoria, hospital_id - ID do hospital (automático), db - sessão do banco]
# [SAIDA: dict - mensagem de sucesso ou exceção]
# [DEPENDENCIAS: CategoryService, require_hospital]
@router.delete("/{public_id}")
def delete_category(
    public_id: UUID,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    category_service = CategoryService(db)
    category_service.delete_category(public_id, hospital_id)
    return {"message": "Category deleted successfully"}
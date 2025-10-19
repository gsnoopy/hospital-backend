from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.item_service import ItemService
from app.schemas.items import ItemCreate, ItemUpdate, ItemResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_hospital
from uuid import UUID
from typing import Optional


# [ITEM ROUTER]
# [Router FastAPI para endpoints CRUD de itens com prefixo /items]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de itens]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/items", tags=["items"])


# [CREATE ITEM]
# [Endpoint POST para criar um novo item - requer autenticação]
# [ENTRADA: item_data - dados do item via ItemCreate, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: ItemResponse - item criado (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: ItemService, require_auth]
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_data: ItemCreate,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    return item_service.create_item(item_data, hospital_id)


# [GET ITEMS]
# [Endpoint GET para listar itens com paginação e busca opcional - requer autenticação]
# [ENTRADA: search - termo de busca opcional, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[ItemResponse] - lista paginada de itens]
# [DEPENDENCIAS: PaginationParams, ItemService, require_auth]
@router.get("/", response_model=PaginatedResponse[ItemResponse])
def get_items(
    search: Optional[str] = Query(None, description="Search term for item names"),
    page: int = 1,
    size: int = 10,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    item_service = ItemService(db)

    if search:
        return item_service.search_items(search, pagination, hospital_id)
    else:
        return item_service.get_paginated_items(pagination, hospital_id)


# [GET ITEM]
# [Endpoint GET para buscar um item pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público do item, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: ItemResponse - dados do item ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: ItemService, require_auth]
@router.get("/{public_id}", response_model=ItemResponse)
def get_item(
    public_id: UUID,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    return item_service.get_item_by_public_id(public_id, hospital_id)


# [GET ITEMS BY SUBCATEGORY]
# [Endpoint GET para buscar itens por subcategoria - requer autenticação]
# [ENTRADA: subcategory_public_id - UUID público da subcategoria, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[ItemResponse] - lista paginada de itens da subcategoria]
# [DEPENDENCIAS: PaginationParams, ItemService, require_auth]
@router.get("/subcategory/{subcategory_public_id}", response_model=PaginatedResponse[ItemResponse])
def get_items_by_subcategory(
    subcategory_public_id: UUID,
    page: int = 1,
    size: int = 10,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    item_service = ItemService(db)
    return item_service.get_items_by_subcategory(subcategory_public_id, pagination, hospital_id)


# [UPDATE ITEM]
# [Endpoint PUT para atualizar um item - requer autenticação]
# [ENTRADA: public_id - UUID público do item, item_data - dados de atualização, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: ItemResponse - item atualizado ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: ItemService, require_auth]
@router.put("/{public_id}", response_model=ItemResponse)
def update_item(
    public_id: UUID,
    item_data: ItemUpdate,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    return item_service.update_item(public_id, item_data, hospital_id)


# [DELETE ITEM]
# [Endpoint DELETE para remover um item - requer autenticação]
# [ENTRADA: public_id - UUID público do item, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: dict - mensagem de sucesso ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: ItemService, require_auth]
@router.delete("/{public_id}")
def delete_item(
    public_id: UUID,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    item_service.delete_item(public_id, hospital_id)
    return {"message": "Item deleted successfully"}


# [SEARCH ITEMS BY SIMILAR NAMES]
# [Endpoint GET para buscar itens por similar_names - requer autenticação]
# [ENTRADA: search - termo de busca, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[ItemResponse] - lista paginada de itens]
# [DEPENDENCIAS: PaginationParams, ItemService, require_auth]
@router.get("/search/similar-names", response_model=PaginatedResponse[ItemResponse])
def search_items_by_similar_names(
    search: str = Query(..., description="Search term for similar names"),
    page: int = 1,
    size: int = 10,
    hospital_id: int = Depends(require_hospital),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    item_service = ItemService(db)
    return item_service.search_items_by_similar_names(search, pagination, hospital_id)

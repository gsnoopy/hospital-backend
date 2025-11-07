from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.hospital_context import HospitalContext
from app.services.item_service import ItemService
from app.schemas.items import ItemCreate, ItemUpdate, ItemResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_role
from uuid import UUID
from typing import Optional


# [ITEM ROUTER]
# [Router FastAPI para endpoints CRUD de itens com prefixo /items]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de itens]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/items", tags=["items"])


# [CREATE ITEM]
# [Endpoint POST para criar um novo item - requer Desenvolvedor, Administrador ou Gerente]
# [ENTRADA: item_data - dados do item, context - contexto de hospital, db - sessão do banco]
# [SAIDA: ItemResponse - item criado (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: ItemService, require_role_and_hospital, HospitalContext]
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_data: ItemCreate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    return item_service.create_item(item_data, context.hospital_id)


# [GET ITEMS]
# [Endpoint GET para listar itens - Desenvolvedor vê todos, outros veem apenas do próprio hospital]
# [ENTRADA: search - termo de busca opcional, search_type - tipo de busca (name, similar_names, unified), page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[ItemResponse] - lista paginada de itens]
# [DEPENDENCIAS: PaginationParams, ItemService, require_role_and_hospital, HospitalContext]
@router.get("/", response_model=PaginatedResponse[ItemResponse])
def get_items(
    search: Optional[str] = Query(None, description="Search term for item names or similar names"),
    search_type: Optional[str] = Query("unified", description="Search type: 'name', 'similar_names', or 'unified' (default)"),
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    item_service = ItemService(db)

    if search:
        if search_type == "name":
            return item_service.search_items(search, pagination, context.hospital_id)
        elif search_type == "similar_names":
            return item_service.search_items_by_similar_names(search, pagination, context.hospital_id)
        else:  # unified (default)
            return item_service.search_items_unified(search, pagination, context.hospital_id)
    else:
        return item_service.get_paginated_items(pagination, context.hospital_id)


# [GET ITEM]
# [Endpoint GET para buscar um item pelo UUID público]
# [ENTRADA: public_id - UUID público do item, context - contexto de hospital, db - sessão do banco]
# [SAIDA: ItemResponse - dados do item ou exceção]
# [DEPENDENCIAS: ItemService, require_role_and_hospital, HospitalContext]
@router.get("/{public_id}", response_model=ItemResponse)
def get_item(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    return item_service.get_item_by_public_id(public_id, context.hospital_id)


# [GET ITEMS BY SUBCATEGORY]
# [Endpoint GET para buscar itens por subcategoria]
# [ENTRADA: subcategory_public_id - UUID público da subcategoria, page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[ItemResponse] - lista paginada de itens da subcategoria]
# [DEPENDENCIAS: PaginationParams, ItemService, require_role_and_hospital, HospitalContext]
@router.get("/subcategory/{subcategory_public_id}", response_model=PaginatedResponse[ItemResponse])
def get_items_by_subcategory(
    subcategory_public_id: UUID,
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    item_service = ItemService(db)
    return item_service.get_items_by_subcategory(subcategory_public_id, pagination, context.hospital_id)


# [UPDATE ITEM]
# [Endpoint PUT para atualizar um item]
# [ENTRADA: public_id - UUID público do item, item_data - dados de atualização, context - contexto de hospital, db - sessão do banco]
# [SAIDA: ItemResponse - item atualizado ou exceção]
# [DEPENDENCIAS: ItemService, require_role_and_hospital, HospitalContext]
@router.put("/{public_id}", response_model=ItemResponse)
def update_item(
    public_id: UUID,
    item_data: ItemUpdate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    return item_service.update_item(public_id, item_data, context.hospital_id)


# [DELETE ITEM]
# [Endpoint DELETE para remover um item]
# [ENTRADA: public_id - UUID público do item, context - contexto de hospital, db - sessão do banco]
# [SAIDA: dict - mensagem de sucesso ou exceção]
# [DEPENDENCIAS: ItemService, require_role_and_hospital, HospitalContext]
@router.delete("/{public_id}")
def delete_item(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    item_service = ItemService(db)
    item_service.delete_item(public_id, context.hospital_id)
    return {"message": "Item deleted successfully"}


# [SEARCH ITEMS BY SIMILAR NAMES]
# [Endpoint GET para buscar itens por similar_names]
# [ENTRADA: search - termo de busca, page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[ItemResponse] - lista paginada de itens]
# [DEPENDENCIAS: PaginationParams, ItemService, require_role_and_hospital, HospitalContext]
@router.get("/search/similar-names", response_model=PaginatedResponse[ItemResponse])
def search_items_by_similar_names(
    search: str = Query(..., description="Search term for similar names"),
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    item_service = ItemService(db)
    return item_service.search_items_by_similar_names(search, pagination, context.hospital_id)

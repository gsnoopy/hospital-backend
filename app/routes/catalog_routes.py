from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.catalog_service import CatalogService
from app.schemas.catalog import CatalogCreate, CatalogUpdate, CatalogResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_auth
from app.models.user import User
from uuid import UUID
from typing import Optional


# [CATALOG ROUTER]
# [Router FastAPI para endpoints CRUD de catálogos com prefixo /catalog]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de catálogos]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/catalog", tags=["catalog"])


# [CREATE CATALOG]
# [Endpoint POST para criar um novo item de catálogo - requer autenticação]
# [ENTRADA: catalog_data - dados do catálogo via CatalogCreate, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CatalogResponse - catálogo criado (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: CatalogService, require_auth]
@router.post("/", response_model=CatalogResponse, status_code=status.HTTP_201_CREATED)
def create_catalog(
    catalog_data: CatalogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    catalog_service = CatalogService(db)
    return catalog_service.create_catalog(catalog_data)


# [GET CATALOGS]
# [Endpoint GET para listar catálogos com paginação e busca opcional - requer autenticação]
# [ENTRADA: search - termo de busca opcional, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[CatalogResponse] - lista paginada de catálogos]
# [DEPENDENCIAS: PaginationParams, CatalogService, require_auth]
@router.get("/", response_model=PaginatedResponse[CatalogResponse])
def get_catalogs(
    search: Optional[str] = Query(None, description="Search term for catalog names"),
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    catalog_service = CatalogService(db)

    if search:
        return catalog_service.search_catalogs(search, pagination)
    else:
        return catalog_service.get_paginated_catalogs(pagination)


# [GET CATALOG]
# [Endpoint GET para buscar um catálogo pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público do catálogo, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CatalogResponse - dados do catálogo ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: CatalogService, require_auth]
@router.get("/{public_id}", response_model=CatalogResponse)
def get_catalog(
    public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    catalog_service = CatalogService(db)
    return catalog_service.get_catalog_by_public_id(public_id)


# [GET CATALOG BY NAME]
# [Endpoint GET para buscar um catálogo pelo nome - requer autenticação]
# [ENTRADA: name - nome do catálogo, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CatalogResponse - dados do catálogo ou 404 se não encontrado]
# [DEPENDENCIAS: CatalogService, require_auth]
@router.get("/name/{name}", response_model=CatalogResponse)
def get_catalog_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    catalog_service = CatalogService(db)
    catalog = catalog_service.get_catalog_by_name(name)

    if not catalog:
        from app.core.exceptions import ResourceNotFoundException
        raise ResourceNotFoundException("Catalog", name)

    return catalog


# [UPDATE CATALOG]
# [Endpoint PUT para atualizar um catálogo - requer autenticação]
# [ENTRADA: public_id - UUID público do catálogo, catalog_data - dados de atualização, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: CatalogResponse - catálogo atualizado ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: CatalogService, require_auth]
@router.put("/{public_id}", response_model=CatalogResponse)
def update_catalog(
    public_id: UUID,
    catalog_data: CatalogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    catalog_service = CatalogService(db)
    return catalog_service.update_catalog(public_id, catalog_data)


# [DELETE CATALOG]
# [Endpoint DELETE para remover um catálogo - requer autenticação]
# [ENTRADA: public_id - UUID público do catálogo, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: dict - mensagem de sucesso ou exceção ResourceNotFoundException]
# [DEPENDENCIAS: CatalogService, require_auth]
@router.delete("/{public_id}")
def delete_catalog(
    public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    catalog_service = CatalogService(db)
    catalog_service.delete_catalog(public_id)
    return {"message": "Catalog deleted successfully"}
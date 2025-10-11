from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.catalog_repository import CatalogRepository
from app.schemas.catalog import CatalogCreate, CatalogUpdate
from app.models.catalog import Catalog
from app.validators.catalog_validator import CatalogValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [CATALOG SERVICE]
# [Serviço para gestão de catálogos com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância CatalogService configurada]
# [DEPENDENCIAS: CatalogRepository, CatalogValidator]
class CatalogService:

    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de catálogo]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: CatalogRepository, CatalogValidator]
    def __init__(self, db: Session):
        self.catalog_repository = CatalogRepository(db)
        self.catalog_validator = CatalogValidator()

    # [CREATE CATALOG]
    # [Cria novo catálogo com validação e verificação de duplicatas]
    # [ENTRADA: catalog_data - dados do catálogo via CatalogCreate]
    # [SAIDA: Catalog - catálogo criado ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.catalog_validator, self.catalog_repository]
    def create_catalog(self, catalog_data: CatalogCreate) -> Catalog:
        validation_result = self.catalog_validator.validate(catalog_data)
        if not validation_result.is_valid:
            errors = validation_result.get_errors_by_field()
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(f"{field}: {msg}")

            raise HTTPException(
                status_code=422,
                detail={
                    "error": True,
                    "message": f"Validation error: {'; '.join(error_messages)}",
                    "status_code": 422
                }
            )

        # Check for unique constraints
        if self.catalog_repository.get_by_name(catalog_data.name):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Catalog with name '{catalog_data.name}' already exists",
                    "status_code": 409
                }
            )

        catalog = self.catalog_repository.create(catalog_data)
        return catalog

    # [GET CATALOG BY PUBLIC ID]
    # [Busca um catálogo pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do catálogo]
    # [SAIDA: Catalog - catálogo encontrado ou exceção se não encontrado]
    # [DEPENDENCIAS: self.catalog_repository]
    def get_catalog_by_public_id(self, public_id: UUID) -> Catalog:
        catalog = self.catalog_repository.get_by_public_id(public_id)
        if not catalog:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Catalog with ID '{public_id}' not found",
                    "status_code": 404
                }
            )
        return catalog

    # [GET CATALOG BY NAME]
    # [Busca um catálogo pelo seu nome]
    # [ENTRADA: name - nome do catálogo]
    # [SAIDA: Optional[Catalog] - catálogo encontrado ou None]
    # [DEPENDENCIAS: self.catalog_repository]
    def get_catalog_by_name(self, name: str) -> Optional[Catalog]:
        return self.catalog_repository.get_by_name(name)

    # [GET PAGINATED CATALOGS]
    # [Busca catálogos com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[Catalog] - catálogos paginados com metadados]
    # [DEPENDENCIAS: self.catalog_repository, PaginatedResponse]
    def get_paginated_catalogs(self, pagination: PaginationParams) -> PaginatedResponse[Catalog]:
        catalogs = self.catalog_repository.get_all(
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.catalog_repository.get_total_count()

        return PaginatedResponse.create(
            items=catalogs,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [SEARCH CATALOGS]
    # [Busca catálogos por termo de pesquisa com paginação]
    # [ENTRADA: search_term - termo de busca, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[Catalog] - catálogos encontrados paginados]
    # [DEPENDENCIAS: self.catalog_repository, PaginatedResponse]
    def search_catalogs(self, search_term: str, pagination: PaginationParams) -> PaginatedResponse[Catalog]:
        catalogs = self.catalog_repository.search_by_name(
            search_term=search_term,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.catalog_repository.get_search_count(search_term)

        return PaginatedResponse.create(
            items=catalogs,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE CATALOG]
    # [Atualiza um catálogo existente]
    # [ENTRADA: public_id - UUID público do catálogo, catalog_data - dados de atualização]
    # [SAIDA: Catalog - catálogo atualizado ou exceção se não encontrado]
    # [DEPENDENCIAS: self.catalog_repository]
    def update_catalog(self, public_id: UUID, catalog_data: CatalogUpdate) -> Catalog:
        catalog = self.catalog_repository.get_by_public_id(public_id)
        if not catalog:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Catalog with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        # Check for conflicts if name is being updated
        if catalog_data.name and catalog_data.name != catalog.name:
            existing_catalog = self.catalog_repository.get_by_name(catalog_data.name)
            if existing_catalog:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Catalog with name '{catalog_data.name}' already exists",
                        "status_code": 409
                    }
                )

        return self.catalog_repository.update(catalog, catalog_data)

    # [DELETE CATALOG]
    # [Remove um catálogo do sistema]
    # [ENTRADA: public_id - UUID público do catálogo a ser removido]
    # [SAIDA: None - exceção se não encontrado]
    # [DEPENDENCIAS: self.catalog_repository]
    def delete_catalog(self, public_id: UUID) -> None:
        catalog = self.catalog_repository.get_by_public_id(public_id)
        if not catalog:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Catalog with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        self.catalog_repository.delete(catalog)
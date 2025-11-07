from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.item_repository import ItemRepository
from app.repositories.subcategory_repository import SubCategoryRepository
from app.repositories.hospital_repository import HospitalRepository
from app.schemas.items import ItemCreate, ItemUpdate
from app.models.items import Item
from app.validators.item_validator import ItemValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [ITEM SERVICE]
# [Serviço para gestão de itens com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância ItemService configurada]
# [DEPENDENCIAS: ItemRepository, SubCategoryRepository, HospitalRepository, ItemValidator]
class ItemService:

    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de item]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: ItemRepository, SubCategoryRepository, HospitalRepository, ItemValidator]
    def __init__(self, db: Session):
        self.item_repository = ItemRepository(db)
        self.subcategory_repository = SubCategoryRepository(db)
        self.hospital_repository = HospitalRepository(db)
        self.item_validator = ItemValidator()

    # [CREATE ITEM]
    # [Cria novo item com validação e verificação de duplicatas]
    # [ENTRADA: item_data - dados do item via ItemCreate, hospital_id - ID interno do hospital]
    # [SAIDA: Item - item criado ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.item_validator, self.item_repository, self.subcategory_repository]
    def create_item(self, item_data: ItemCreate, hospital_id: int) -> Item:
        validation_result = self.item_validator.validate(item_data)
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

        # Check if internal_code is unique within the hospital
        if item_data.internal_code:
            if self.item_repository.get_by_internal_code(item_data.internal_code, hospital_id):
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Item with internal code '{item_data.internal_code}' already exists",
                        "status_code": 409
                    }
                )

        # Resolve foreign key relationships - check subcategory belongs to hospital
        subcategory = self.subcategory_repository.get_by_public_id(item_data.subcategory_id, hospital_id)
        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"SubCategory with ID '{item_data.subcategory_id}' not found",
                    "status_code": 404
                }
            )

        item = self.item_repository.create(item_data, subcategory.id, hospital_id)
        return item

    # [GET ITEM BY PUBLIC ID]
    # [Busca um item pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do item, hospital_id - ID interno do hospital]
    # [SAIDA: Item - item encontrado ou exceção se não encontrado]
    # [DEPENDENCIAS: self.item_repository]
    def get_item_by_public_id(self, public_id: UUID, hospital_id: int) -> Item:
        item = self.item_repository.get_by_public_id(public_id, hospital_id)
        if not item:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Item with ID '{public_id}' not found",
                    "status_code": 404
                }
            )
        return item

    # [GET PAGINATED ITEMS]
    # [Busca itens com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[Item] - itens paginados com metadados]
    # [DEPENDENCIAS: self.item_repository, PaginatedResponse]
    def get_paginated_items(self, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[Item]:
        items = self.item_repository.get_all(
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.item_repository.get_total_count(hospital_id)

        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET ITEMS BY SUBCATEGORY]
    # [Busca itens por subcategoria com paginação usando UUID público]
    # [ENTRADA: subcategory_public_id - UUID público da subcategoria, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[Item] - itens paginados da subcategoria]
    # [DEPENDENCIAS: self.item_repository, self.subcategory_repository, PaginatedResponse]
    def get_items_by_subcategory(self, subcategory_public_id: UUID, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[Item]:
        subcategory = self.subcategory_repository.get_by_public_id(subcategory_public_id, hospital_id)
        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"SubCategory with ID '{subcategory_public_id}' not found",
                    "status_code": 404
                }
            )

        items = self.item_repository.get_by_subcategory_id(
            subcategory_id=subcategory.id,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.item_repository.get_subcategory_count(subcategory.id, hospital_id)

        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [SEARCH ITEMS]
    # [Busca itens por termo de pesquisa com paginação]
    # [ENTRADA: search_term - termo de busca, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[Item] - itens encontrados paginados]
    # [DEPENDENCIAS: self.item_repository, PaginatedResponse]
    def search_items(self, search_term: str, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[Item]:
        items = self.item_repository.search_by_name(
            search_term=search_term,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.item_repository.get_search_count(search_term, hospital_id)

        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [SEARCH ITEMS BY SIMILAR NAMES]
    # [Busca itens por similar_names com paginação]
    # [ENTRADA: search_term - termo de busca, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[Item] - itens encontrados paginados]
    # [DEPENDENCIAS: self.item_repository, PaginatedResponse]
    def search_items_by_similar_names(self, search_term: str, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[Item]:
        items = self.item_repository.search_by_similar_names(
            search_term=search_term,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.item_repository.get_similar_names_search_count(search_term, hospital_id)

        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [SEARCH ITEMS UNIFIED]
    # [Busca unificada por name OU similar_names com paginação]
    # [ENTRADA: search_term - termo de busca, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[Item] - itens encontrados paginados]
    # [DEPENDENCIAS: self.item_repository, PaginatedResponse]
    def search_items_unified(self, search_term: str, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[Item]:
        items = self.item_repository.search_unified(
            search_term=search_term,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.item_repository.get_unified_search_count(search_term, hospital_id)

        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE ITEM]
    # [Atualiza um item existente]
    # [ENTRADA: public_id - UUID público do item, item_data - dados de atualização, hospital_id - ID interno do hospital]
    # [SAIDA: Item - item atualizado ou exceção se não encontrado]
    # [DEPENDENCIAS: self.item_repository, self.subcategory_repository]
    def update_item(self, public_id: UUID, item_data: ItemUpdate, hospital_id: int) -> Item:
        item = self.item_repository.get_by_public_id(public_id, hospital_id)
        if not item:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Item with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        # Check for conflicts if internal_code is being updated
        if item_data.internal_code and item_data.internal_code != item.internal_code:
            existing_item = self.item_repository.get_by_internal_code(item_data.internal_code, hospital_id)
            if existing_item:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Item with internal code '{item_data.internal_code}' already exists",
                        "status_code": 409
                    }
                )

        # Resolve foreign key relationships if being updated
        subcategory_internal_id = None
        if item_data.subcategory_id:
            subcategory = self.subcategory_repository.get_by_public_id(item_data.subcategory_id, hospital_id)
            if not subcategory:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"SubCategory with ID '{item_data.subcategory_id}' not found",
                        "status_code": 404
                    }
                )
            subcategory_internal_id = subcategory.id

        return self.item_repository.update(item, item_data, subcategory_internal_id)

    # [DELETE ITEM]
    # [Remove um item do sistema]
    # [ENTRADA: public_id - UUID público do item a ser removido, hospital_id - ID interno do hospital]
    # [SAIDA: None - exceção se não encontrado]
    # [DEPENDENCIAS: self.item_repository]
    def delete_item(self, public_id: UUID, hospital_id: int) -> None:
        item = self.item_repository.get_by_public_id(public_id, hospital_id)
        if not item:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Item with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        self.item_repository.delete(item)

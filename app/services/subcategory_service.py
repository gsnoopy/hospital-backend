from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.subcategory_repository import SubCategoryRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.subcategory import SubCategoryCreate, SubCategoryUpdate, SubCategoryResponse
from app.models.subcategories import SubCategory
from app.validators.subcategory_validator import SubCategoryValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [SUBCATEGORY SERVICE]
# [Serviço para gestão de subcategorias com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância SubCategoryService configurada]
# [DEPENDENCIAS: SubCategoryRepository, CategoryRepository, SubCategoryValidator]
class SubCategoryService:

    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de subcategoria]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: SubCategoryRepository, CategoryRepository, SubCategoryValidator]
    def __init__(self, db: Session):
        self.subcategory_repository = SubCategoryRepository(db)
        self.category_repository = CategoryRepository(db)
        self.subcategory_validator = SubCategoryValidator()

    # [CREATE SUBCATEGORY]
    # [Cria nova subcategoria com validação e verificação de duplicatas]
    # [ENTRADA: subcategory_data - dados da subcategoria via SubCategoryCreate, hospital_id - ID interno do hospital]
    # [SAIDA: SubCategory - subcategoria criada ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.subcategory_validator, self.subcategory_repository, self.category_repository]
    def create_subcategory(self, subcategory_data: SubCategoryCreate, hospital_id: int) -> SubCategory:
        validation_result = self.subcategory_validator.validate(subcategory_data)
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

        # Check if category exists and belongs to the same hospital
        category = self.category_repository.get_by_public_id(subcategory_data.category_id, hospital_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Category with ID '{subcategory_data.category_id}' not found",
                    "status_code": 404
                }
            )

        # Check for unique constraints within the hospital
        if self.subcategory_repository.get_by_name(subcategory_data.name, hospital_id):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"SubCategory with name '{subcategory_data.name}' already exists",
                    "status_code": 409
                }
            )

        subcategory = self.subcategory_repository.create(subcategory_data, category.id, hospital_id)
        return subcategory

    # [GET SUBCATEGORY BY PUBLIC ID]
    # [Busca uma subcategoria pelo seu UUID público]
    # [ENTRADA: public_id - UUID público da subcategoria, hospital_id - ID interno do hospital]
    # [SAIDA: SubCategory - subcategoria encontrada ou exceção se não encontrada]
    # [DEPENDENCIAS: self.subcategory_repository]
    def get_subcategory_by_public_id(self, public_id: UUID, hospital_id: int) -> SubCategory:
        subcategory = self.subcategory_repository.get_by_public_id(public_id, hospital_id)
        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"SubCategory with ID '{public_id}' not found",
                    "status_code": 404
                }
            )
        return subcategory

    # [GET SUBCATEGORY BY NAME]
    # [Busca uma subcategoria pelo seu nome]
    # [ENTRADA: name - nome da subcategoria, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[SubCategory] - subcategoria encontrada ou None]
    # [DEPENDENCIAS: self.subcategory_repository]
    def get_subcategory_by_name(self, name: str, hospital_id: int) -> Optional[SubCategory]:
        return self.subcategory_repository.get_by_name(name, hospital_id)

    # [GET SUBCATEGORIES BY CATEGORY]
    # [Busca subcategorias por categoria com paginação]
    # [ENTRADA: category_public_id - UUID público da categoria, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[SubCategory] - subcategorias paginadas da categoria]
    # [DEPENDENCIAS: self.subcategory_repository, self.category_repository, PaginatedResponse]
    def get_subcategories_by_category(self, category_public_id: UUID, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[SubCategory]:
        category = self.category_repository.get_by_public_id(category_public_id, hospital_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Category with ID '{category_public_id}' not found",
                    "status_code": 404
                }
            )

        subcategories = self.subcategory_repository.get_by_category(
            category_id=category.id,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.subcategory_repository.get_total_count_by_category(category.id, hospital_id)

        return PaginatedResponse.create(
            items=subcategories,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET PAGINATED SUBCATEGORIES]
    # [Busca subcategorias com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[SubCategory] - subcategorias paginadas com metadados]
    # [DEPENDENCIAS: self.subcategory_repository, PaginatedResponse]
    def get_paginated_subcategories(self, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[SubCategory]:
        subcategories = self.subcategory_repository.get_all(
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.subcategory_repository.get_total_count(hospital_id)

        return PaginatedResponse.create(
            items=subcategories,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE SUBCATEGORY]
    # [Atualiza uma subcategoria existente]
    # [ENTRADA: public_id - UUID público da subcategoria, subcategory_data - dados de atualização, hospital_id - ID interno do hospital]
    # [SAIDA: SubCategory - subcategoria atualizada ou exceção se não encontrada]
    # [DEPENDENCIAS: self.subcategory_repository, self.category_repository]
    def update_subcategory(self, public_id: UUID, subcategory_data: SubCategoryUpdate, hospital_id: int) -> SubCategory:
        subcategory = self.subcategory_repository.get_by_public_id(public_id, hospital_id)
        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"SubCategory with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        category_internal_id = None

        # Check if category exists if category_id is being updated
        if subcategory_data.category_id:
            category = self.category_repository.get_by_public_id(subcategory_data.category_id, hospital_id)
            if not category:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"Category with ID '{subcategory_data.category_id}' not found",
                        "status_code": 404
                    }
                )
            category_internal_id = category.id

        # Check for conflicts if name is being updated
        if subcategory_data.name and subcategory_data.name != subcategory.name:
            existing_subcategory = self.subcategory_repository.get_by_name(subcategory_data.name, hospital_id)
            if existing_subcategory:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"SubCategory with name '{subcategory_data.name}' already exists",
                        "status_code": 409
                    }
                )

        return self.subcategory_repository.update(subcategory, subcategory_data, category_internal_id)

    # [DELETE SUBCATEGORY]
    # [Remove uma subcategoria do sistema]
    # [ENTRADA: public_id - UUID público da subcategoria a ser removida, hospital_id - ID interno do hospital]
    # [SAIDA: None - exceção se não encontrada]
    # [DEPENDENCIAS: self.subcategory_repository]
    def delete_subcategory(self, public_id: UUID, hospital_id: int) -> None:
        subcategory = self.subcategory_repository.get_by_public_id(public_id, hospital_id)
        if not subcategory:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"SubCategory with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        self.subcategory_repository.delete(subcategory)
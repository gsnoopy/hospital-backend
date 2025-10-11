from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.categories import Category
from app.validators.category_validator import CategoryValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [CATEGORY SERVICE]
# [Serviço para gestão de categorias com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância CategoryService configurada]
# [DEPENDENCIAS: CategoryRepository, CategoryValidator]
class CategoryService:

    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de categoria]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: CategoryRepository, CategoryValidator]
    def __init__(self, db: Session):
        self.category_repository = CategoryRepository(db)
        self.category_validator = CategoryValidator()

    # [CREATE CATEGORY]
    # [Cria nova categoria com validação e verificação de duplicatas]
    # [ENTRADA: category_data - dados da categoria via CategoryCreate]
    # [SAIDA: Category - categoria criada ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.category_validator, self.category_repository]
    def create_category(self, category_data: CategoryCreate) -> Category:
        validation_result = self.category_validator.validate(category_data)
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
        if self.category_repository.get_by_name(category_data.name):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Category with name '{category_data.name}' already exists",
                    "status_code": 409
                }
            )

        category = self.category_repository.create(category_data)
        return category

    # [GET CATEGORY BY PUBLIC ID]
    # [Busca uma categoria pelo seu UUID público]
    # [ENTRADA: public_id - UUID público da categoria]
    # [SAIDA: Category - categoria encontrada ou exceção se não encontrada]
    # [DEPENDENCIAS: self.category_repository]
    def get_category_by_public_id(self, public_id: UUID) -> Category:
        category = self.category_repository.get_by_public_id(public_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Category with ID '{public_id}' not found",
                    "status_code": 404
                }
            )
        return category

    # [GET CATEGORY BY NAME]
    # [Busca uma categoria pelo seu nome]
    # [ENTRADA: name - nome da categoria]
    # [SAIDA: Optional[Category] - categoria encontrada ou None]
    # [DEPENDENCIAS: self.category_repository]
    def get_category_by_name(self, name: str) -> Optional[Category]:
        return self.category_repository.get_by_name(name)

    # [GET PAGINATED CATEGORIES]
    # [Busca categorias com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[Category] - categorias paginadas com metadados]
    # [DEPENDENCIAS: self.category_repository, PaginatedResponse]
    def get_paginated_categories(self, pagination: PaginationParams) -> PaginatedResponse[Category]:
        categories = self.category_repository.get_all(
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.category_repository.get_total_count()

        return PaginatedResponse.create(
            items=categories,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE CATEGORY]
    # [Atualiza uma categoria existente]
    # [ENTRADA: public_id - UUID público da categoria, category_data - dados de atualização]
    # [SAIDA: Category - categoria atualizada ou exceção se não encontrada]
    # [DEPENDENCIAS: self.category_repository]
    def update_category(self, public_id: UUID, category_data: CategoryUpdate) -> Category:
        category = self.category_repository.get_by_public_id(public_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Category with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        # Check for conflicts if name is being updated
        if category_data.name and category_data.name != category.name:
            existing_category = self.category_repository.get_by_name(category_data.name)
            if existing_category:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Category with name '{category_data.name}' already exists",
                        "status_code": 409
                    }
                )

        return self.category_repository.update(category, category_data)

    # [DELETE CATEGORY]
    # [Remove uma categoria do sistema]
    # [ENTRADA: public_id - UUID público da categoria a ser removida]
    # [SAIDA: None - exceção se não encontrada]
    # [DEPENDENCIAS: self.category_repository]
    def delete_category(self, public_id: UUID) -> None:
        category = self.category_repository.get_by_public_id(public_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Category with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        self.category_repository.delete(category)
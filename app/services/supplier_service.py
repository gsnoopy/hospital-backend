from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.supplier_repository import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.models.supplier import Supplier
from app.validators.supplier_validator import SupplierValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from uuid import UUID


# [SUPPLIER SERVICE]
# [Serviço para gestão de fornecedores com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância SupplierService configurada]
# [DEPENDENCIAS: SupplierRepository, SupplierValidator]
class SupplierService:

    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de fornecedor]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: SupplierRepository, SupplierValidator]
    def __init__(self, db: Session):
        self.supplier_repository = SupplierRepository(db)
        self.supplier_validator = SupplierValidator()

    # [CREATE SUPPLIER]
    # [Cria novo fornecedor com validação e verificação de duplicatas]
    # [ENTRADA: supplier_data - dados do fornecedor via SupplierCreate, hospital_id - ID interno do hospital]
    # [SAIDA: Supplier - fornecedor criado ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.supplier_validator, self.supplier_repository]
    def create_supplier(self, supplier_data: SupplierCreate, hospital_id: int) -> Supplier:
        validation_result = self.supplier_validator.validate(supplier_data)
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

        # Check if document is unique within the hospital
        if self.supplier_repository.get_by_document(supplier_data.document, hospital_id):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Supplier with document '{supplier_data.document}' already exists",
                    "status_code": 409
                }
            )

        # Check if email is unique within the hospital
        if self.supplier_repository.get_by_email(supplier_data.email, hospital_id):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Supplier with email '{supplier_data.email}' already exists",
                    "status_code": 409
                }
            )

        supplier = self.supplier_repository.create(supplier_data, hospital_id)
        return supplier

    # [GET SUPPLIER BY PUBLIC ID]
    # [Busca um fornecedor pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do fornecedor, hospital_id - ID interno do hospital]
    # [SAIDA: Supplier - fornecedor encontrado ou exceção se não encontrado]
    # [DEPENDENCIAS: self.supplier_repository]
    def get_supplier_by_public_id(self, public_id: UUID, hospital_id: int) -> Supplier:
        supplier = self.supplier_repository.get_by_public_id(public_id, hospital_id)
        if not supplier:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Supplier with ID '{public_id}' not found",
                    "status_code": 404
                }
            )
        return supplier

    # [GET PAGINATED SUPPLIERS]
    # [Busca fornecedores com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[Supplier] - fornecedores paginados com metadados]
    # [DEPENDENCIAS: self.supplier_repository, PaginatedResponse]
    def get_paginated_suppliers(self, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[Supplier]:
        suppliers = self.supplier_repository.get_all(
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.supplier_repository.get_total_count(hospital_id)

        return PaginatedResponse.create(
            items=suppliers,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [SEARCH SUPPLIERS]
    # [Busca fornecedores por termo de pesquisa com paginação]
    # [ENTRADA: search_term - termo de busca, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[Supplier] - fornecedores encontrados paginados]
    # [DEPENDENCIAS: self.supplier_repository, PaginatedResponse]
    def search_suppliers(self, search_term: str, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[Supplier]:
        suppliers = self.supplier_repository.search_by_name(
            search_term=search_term,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.supplier_repository.get_search_count(search_term, hospital_id)

        return PaginatedResponse.create(
            items=suppliers,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE SUPPLIER]
    # [Atualiza um fornecedor existente]
    # [ENTRADA: public_id - UUID público do fornecedor, supplier_data - dados de atualização, hospital_id - ID interno do hospital]
    # [SAIDA: Supplier - fornecedor atualizado ou exceção se não encontrado]
    # [DEPENDENCIAS: self.supplier_repository]
    def update_supplier(self, public_id: UUID, supplier_data: SupplierUpdate, hospital_id: int) -> Supplier:
        supplier = self.supplier_repository.get_by_public_id(public_id, hospital_id)
        if not supplier:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Supplier with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        # Check for conflicts if document is being updated
        if supplier_data.document and supplier_data.document != supplier.document:
            existing_supplier = self.supplier_repository.get_by_document(supplier_data.document, hospital_id)
            if existing_supplier:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Supplier with document '{supplier_data.document}' already exists",
                        "status_code": 409
                    }
                )

        # Check for conflicts if email is being updated
        if supplier_data.email and supplier_data.email != supplier.email:
            existing_supplier = self.supplier_repository.get_by_email(supplier_data.email, hospital_id)
            if existing_supplier:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Supplier with email '{supplier_data.email}' already exists",
                        "status_code": 409
                    }
                )

        return self.supplier_repository.update(supplier, supplier_data)

    # [DELETE SUPPLIER]
    # [Remove um fornecedor do sistema]
    # [ENTRADA: public_id - UUID público do fornecedor a ser removido, hospital_id - ID interno do hospital]
    # [SAIDA: None - exceção se não encontrado]
    # [DEPENDENCIAS: self.supplier_repository]
    def delete_supplier(self, public_id: UUID, hospital_id: int) -> None:
        supplier = self.supplier_repository.get_by_public_id(public_id, hospital_id)
        if not supplier:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Supplier with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        self.supplier_repository.delete(supplier)

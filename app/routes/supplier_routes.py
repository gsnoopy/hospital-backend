from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.hospital_context import HospitalContext
from app.services.supplier_service import SupplierService
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_role
from uuid import UUID
from typing import Optional


# [SUPPLIER ROUTER]
# [Router FastAPI para endpoints CRUD de fornecedores com prefixo /suppliers]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de fornecedores]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/suppliers", tags=["suppliers"])


# [CREATE SUPPLIER]
# [Endpoint POST para criar um novo fornecedor - requer Administrador ou Gerente]
# [ENTRADA: supplier_data - dados do fornecedor, context - contexto de hospital, db - sessão do banco]
# [SAIDA: SupplierResponse - fornecedor criado (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: SupplierService, require_role, HospitalContext]
@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier_data: SupplierCreate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    supplier_service = SupplierService(db)
    return supplier_service.create_supplier(supplier_data, context.hospital_id)


# [GET SUPPLIERS]
# [Endpoint GET para listar fornecedores - filtra por hospital do usuário logado]
# [ENTRADA: search - termo de busca opcional, page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[SupplierResponse] - lista paginada de fornecedores]
# [DEPENDENCIAS: PaginationParams, SupplierService, require_role, HospitalContext]
@router.get("/", response_model=PaginatedResponse[SupplierResponse])
def get_suppliers(
    search: Optional[str] = Query(None, description="Search term for supplier names"),
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    supplier_service = SupplierService(db)

    if search:
        return supplier_service.search_suppliers(search, pagination, context.hospital_id)
    else:
        return supplier_service.get_paginated_suppliers(pagination, context.hospital_id)


# [GET SUPPLIER]
# [Endpoint GET para buscar um fornecedor pelo UUID público]
# [ENTRADA: public_id - UUID público do fornecedor, context - contexto de hospital, db - sessão do banco]
# [SAIDA: SupplierResponse - dados do fornecedor ou exceção]
# [DEPENDENCIAS: SupplierService, require_role, HospitalContext]
@router.get("/{public_id}", response_model=SupplierResponse)
def get_supplier(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    supplier_service = SupplierService(db)
    return supplier_service.get_supplier_by_public_id(public_id, context.hospital_id)


# [UPDATE SUPPLIER]
# [Endpoint PUT para atualizar um fornecedor]
# [ENTRADA: public_id - UUID público do fornecedor, supplier_data - dados de atualização, context - contexto de hospital, db - sessão do banco]
# [SAIDA: SupplierResponse - fornecedor atualizado ou exceção]
# [DEPENDENCIAS: SupplierService, require_role, HospitalContext]
@router.put("/{public_id}", response_model=SupplierResponse)
def update_supplier(
    public_id: UUID,
    supplier_data: SupplierUpdate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    supplier_service = SupplierService(db)
    return supplier_service.update_supplier(public_id, supplier_data, context.hospital_id)


# [DELETE SUPPLIER]
# [Endpoint DELETE para remover um fornecedor]
# [ENTRADA: public_id - UUID público do fornecedor, context - contexto de hospital, db - sessão do banco]
# [SAIDA: dict - mensagem de sucesso ou exceção]
# [DEPENDENCIAS: SupplierService, require_role, HospitalContext]
@router.delete("/{public_id}")
def delete_supplier(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    supplier_service = SupplierService(db)
    supplier_service.delete_supplier(public_id, context.hospital_id)
    return {"message": "Supplier deleted successfully"}

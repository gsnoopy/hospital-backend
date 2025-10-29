from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.hospital_context import HospitalContext
from app.services.public_acquisition_service import PublicAcquisitionService
from app.schemas.public_acquisition import PublicAcquisitionCreate, PublicAcquisitionUpdate, PublicAcquisitionResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_role
from uuid import UUID
from typing import Optional


# [PUBLIC ACQUISITION ROUTER]
# [Router FastAPI para endpoints CRUD de licitações públicas com prefixo /public-acquisitions]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de licitações]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/public-acquisitions", tags=["public-acquisitions"])


# [CREATE PUBLIC ACQUISITION]
# [Endpoint POST para criar uma nova licitação - requer Administrador ou Gerente]
# [ENTRADA: public_acquisition_data - dados da licitação, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PublicAcquisitionResponse - licitação criada (status 201) ou exceções personalizadas]
# [DEPENDENCIAS: PublicAcquisitionService, require_role, HospitalContext]
@router.post("/", response_model=PublicAcquisitionResponse, status_code=status.HTTP_201_CREATED)
def create_public_acquisition(
    public_acquisition_data: PublicAcquisitionCreate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    public_acquisition_service = PublicAcquisitionService(db)
    return public_acquisition_service.create_public_acquisition(public_acquisition_data, context.hospital_id)


# [GET PUBLIC ACQUISITIONS]
# [Endpoint GET para listar licitações - filtra por hospital do usuário logado]
# [ENTRADA: search - termo de busca opcional, search_by - campo de busca (title ou code), page - número da página, size - itens por página, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PaginatedResponse[PublicAcquisitionResponse] - lista paginada de licitações]
# [DEPENDENCIAS: PaginationParams, PublicAcquisitionService, require_role, HospitalContext]
@router.get("/", response_model=PaginatedResponse[PublicAcquisitionResponse])
def get_public_acquisitions(
    search: Optional[str] = Query(None, description="Search term for public acquisition title or code"),
    search_by: Optional[str] = Query("title", description="Search by 'title' or 'code'"),
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    public_acquisition_service = PublicAcquisitionService(db)

    if search:
        if search_by == "code":
            return public_acquisition_service.search_public_acquisitions_by_code(search, pagination, context.hospital_id)
        else:
            return public_acquisition_service.search_public_acquisitions(search, pagination, context.hospital_id)
    else:
        return public_acquisition_service.get_paginated_public_acquisitions(pagination, context.hospital_id)


# [GET PUBLIC ACQUISITION]
# [Endpoint GET para buscar uma licitação pelo UUID público]
# [ENTRADA: public_id - UUID público da licitação, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PublicAcquisitionResponse - dados da licitação ou exceção]
# [DEPENDENCIAS: PublicAcquisitionService, require_role, HospitalContext]
@router.get("/{public_id}", response_model=PublicAcquisitionResponse)
def get_public_acquisition(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    public_acquisition_service = PublicAcquisitionService(db)
    return public_acquisition_service.get_public_acquisition_by_public_id(public_id, context.hospital_id)


# [UPDATE PUBLIC ACQUISITION]
# [Endpoint PUT para atualizar uma licitação]
# [ENTRADA: public_id - UUID público da licitação, public_acquisition_data - dados de atualização, context - contexto de hospital, db - sessão do banco]
# [SAIDA: PublicAcquisitionResponse - licitação atualizada ou exceção]
# [DEPENDENCIAS: PublicAcquisitionService, require_role, HospitalContext]
@router.put("/{public_id}", response_model=PublicAcquisitionResponse)
def update_public_acquisition(
    public_id: UUID,
    public_acquisition_data: PublicAcquisitionUpdate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    public_acquisition_service = PublicAcquisitionService(db)
    return public_acquisition_service.update_public_acquisition(public_id, public_acquisition_data, context.hospital_id)


# [DELETE PUBLIC ACQUISITION]
# [Endpoint DELETE para remover uma licitação]
# [ENTRADA: public_id - UUID público da licitação, context - contexto de hospital, db - sessão do banco]
# [SAIDA: dict - mensagem de sucesso ou exceção]
# [DEPENDENCIAS: PublicAcquisitionService, require_role, HospitalContext]
@router.delete("/{public_id}")
def delete_public_acquisition(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente"])),
    db: Session = Depends(get_db)
):
    public_acquisition_service = PublicAcquisitionService(db)
    public_acquisition_service.delete_public_acquisition(public_id, context.hospital_id)
    return {"message": "Public acquisition deleted successfully"}

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.hospital_context import HospitalContext
from app.services.item_public_acquisition_service import ItemPublicAcquisitionService
from app.schemas.item_public_acquisition import (
    ItemPublicAcquisitionCreate,
    ItemPublicAcquisitionUpdate,
    ItemPublicAcquisitionResponse
)
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_role
from uuid import UUID


# [ITEM PUBLIC ACQUISITION ROUTER]
# [Router FastAPI para endpoints de associação item-licitação-fornecedor]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/item-public-acquisitions", tags=["item-public-acquisitions"])


# [CREATE ASSOCIATION]
# [Endpoint POST para associar item a licitação com fornecedor - requer Administrador ou Gerente]
# [ENTRADA: association_data, context, db]
# [SAIDA: ItemPublicAcquisitionResponse (status 201) ou HTTPException]
# [DEPENDENCIAS: ItemPublicAcquisitionService, require_role, HospitalContext]
@router.post("/", response_model=ItemPublicAcquisitionResponse, status_code=status.HTTP_201_CREATED)
def create_association(
    association_data: ItemPublicAcquisitionCreate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente", "Pregoeiro"])),
    db: Session = Depends(get_db)
):
    service = ItemPublicAcquisitionService(db)
    return service.create_association(association_data, context.hospital_id)


# [GET ITEMS BY PUBLIC ACQUISITION]
# [Endpoint GET para listar todos os itens de uma licitação]
# [ENTRADA: public_acquisition_id, page, size, context, db]
# [SAIDA: PaginatedResponse[ItemPublicAcquisitionResponse]]
# [DEPENDENCIAS: ItemPublicAcquisitionService, require_role, HospitalContext]
@router.get("/by-public-acquisition/{public_acquisition_id}", response_model=PaginatedResponse[ItemPublicAcquisitionResponse])
def get_items_by_public_acquisition(
    public_acquisition_id: UUID,
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente", "Pregoeiro"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    service = ItemPublicAcquisitionService(db)
    return service.get_items_by_public_acquisition(public_acquisition_id, pagination, context.hospital_id)


# [GET PUBLIC ACQUISITIONS BY ITEM]
# [Endpoint GET para listar todas as licitações que contêm um item]
# [ENTRADA: item_id, page, size, context, db]
# [SAIDA: PaginatedResponse[ItemPublicAcquisitionResponse]]
# [DEPENDENCIAS: ItemPublicAcquisitionService, require_role, HospitalContext]
@router.get("/by-item/{item_id}", response_model=PaginatedResponse[ItemPublicAcquisitionResponse])
def get_public_acquisitions_by_item(
    item_id: UUID,
    page: int = 1,
    size: int = 10,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente", "Pregoeiro"])),
    db: Session = Depends(get_db)
):
    pagination = PaginationParams(page=page, size=size)
    service = ItemPublicAcquisitionService(db)
    return service.get_public_acquisitions_by_item(item_id, pagination, context.hospital_id)


# [GET ASSOCIATION]
# [Endpoint GET para buscar uma associação pelo UUID público]
# [ENTRADA: public_id, context, db]
# [SAIDA: ItemPublicAcquisitionResponse ou HTTPException 404]
# [DEPENDENCIAS: ItemPublicAcquisitionService, require_role, HospitalContext]
@router.get("/{public_id}", response_model=ItemPublicAcquisitionResponse)
def get_association(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente", "Pregoeiro"])),
    db: Session = Depends(get_db)
):
    service = ItemPublicAcquisitionService(db)
    return service.get_association_by_public_id(public_id)


# [UPDATE ASSOCIATION]
# [Endpoint PUT para atualizar fornecedor de uma associação]
# [ENTRADA: public_id, association_data, context, db]
# [SAIDA: ItemPublicAcquisitionResponse ou HTTPException 404]
# [DEPENDENCIAS: ItemPublicAcquisitionService, require_role, HospitalContext]
@router.put("/{public_id}", response_model=ItemPublicAcquisitionResponse)
def update_association(
    public_id: UUID,
    association_data: ItemPublicAcquisitionUpdate,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente", "Pregoeiro"])),
    db: Session = Depends(get_db)
):
    service = ItemPublicAcquisitionService(db)
    return service.update_association(public_id, association_data, context.hospital_id)


# [DELETE ASSOCIATION]
# [Endpoint DELETE para remover associação (desassociar item da licitação)]
# [ENTRADA: public_id, context, db]
# [SAIDA: dict - mensagem de sucesso ou HTTPException 404]
# [DEPENDENCIAS: ItemPublicAcquisitionService, require_role, HospitalContext]
@router.delete("/{public_id}")
def delete_association(
    public_id: UUID,
    context: HospitalContext = Depends(require_role(["Administrador", "Gerente", "Pregoeiro"])),
    db: Session = Depends(get_db)
):
    service = ItemPublicAcquisitionService(db)
    service.delete_association(public_id)
    return {"message": "Association deleted successfully"}

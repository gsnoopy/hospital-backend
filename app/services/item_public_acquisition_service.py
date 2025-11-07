from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.item_public_acquisition_repository import ItemPublicAcquisitionRepository
from app.repositories.item_repository import ItemRepository
from app.repositories.public_acquisition_repository import PublicAcquisitionRepository
from app.repositories.supplier_repository import SupplierRepository
from app.schemas.item_public_acquisition import ItemPublicAcquisitionCreate, ItemPublicAcquisitionUpdate
from app.models.item_public_acquisition import ItemPublicAcquisition
from app.schemas.pagination import PaginatedResponse, PaginationParams
from uuid import UUID


# [ITEM PUBLIC ACQUISITION SERVICE]
# [Serviço para gestão de associações item-licitação-fornecedor com validações]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância ItemPublicAcquisitionService configurada]
# [DEPENDENCIAS: ItemPublicAcquisitionRepository, ItemRepository, PublicAcquisitionRepository, SupplierRepository]
class ItemPublicAcquisitionService:

    # [INIT]
    # [Construtor que inicializa o serviço com repositories]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: Repositories]
    def __init__(self, db: Session):
        self.association_repository = ItemPublicAcquisitionRepository(db)
        self.item_repository = ItemRepository(db)
        self.public_acquisition_repository = PublicAcquisitionRepository(db)
        self.supplier_repository = SupplierRepository(db)
        self.db = db

    # [CREATE ASSOCIATION]
    # [Cria nova associação validando existência e escopo de hospital]
    # [ENTRADA: association_data, hospital_id]
    # [SAIDA: ItemPublicAcquisition ou HTTPException]
    # [DEPENDENCIAS: repositories]
    def create_association(self, association_data: ItemPublicAcquisitionCreate, hospital_id: int) -> ItemPublicAcquisition:
        # Validate item exists and belongs to hospital
        item = self.item_repository.get_by_public_id(association_data.item_id, hospital_id)
        if not item:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Item with ID '{association_data.item_id}' not found in this hospital",
                    "status_code": 404
                }
            )

        # Validate public acquisition exists and belongs to hospital
        public_acquisition = self.public_acquisition_repository.get_by_public_id(
            association_data.public_acquisition_id, hospital_id
        )
        if not public_acquisition:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Public acquisition with ID '{association_data.public_acquisition_id}' not found in this hospital",
                    "status_code": 404
                }
            )

        # Validate supplier exists and belongs to hospital
        supplier = self.supplier_repository.get_by_public_id(association_data.supplier_id, hospital_id)
        if not supplier:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Supplier with ID '{association_data.supplier_id}' not found in this hospital",
                    "status_code": 404
                }
            )

        # Check if association already exists
        existing = self.association_repository.get_by_item_and_public_acquisition(
            item.id, public_acquisition.id
        )
        if existing:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": "This item is already associated with this public acquisition",
                    "status_code": 409
                }
            )

        # Create association
        association = self.association_repository.create(
            item.id,
            public_acquisition.id,
            supplier.id,
            association_data.is_holder
        )
        return association

    # [GET ASSOCIATION BY PUBLIC ID]
    # [Busca uma associação pelo UUID público]
    # [ENTRADA: public_id]
    # [SAIDA: ItemPublicAcquisition ou HTTPException]
    # [DEPENDENCIAS: association_repository]
    def get_association_by_public_id(self, public_id: UUID) -> ItemPublicAcquisition:
        association = self.association_repository.get_by_public_id(public_id)
        if not association:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Association with ID '{public_id}' not found",
                    "status_code": 404
                }
            )
        return association

    # [GET ITEMS BY PUBLIC ACQUISITION]
    # [Lista todos os itens de uma licitação com paginação]
    # [ENTRADA: public_acquisition_id, pagination, hospital_id]
    # [SAIDA: PaginatedResponse[ItemPublicAcquisition]]
    # [DEPENDENCIAS: repositories]
    def get_items_by_public_acquisition(
        self, public_acquisition_id: UUID, pagination: PaginationParams, hospital_id: int
    ) -> PaginatedResponse[ItemPublicAcquisition]:
        # Validate public acquisition exists and belongs to hospital
        public_acquisition = self.public_acquisition_repository.get_by_public_id(public_acquisition_id, hospital_id)
        if not public_acquisition:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Public acquisition with ID '{public_acquisition_id}' not found in this hospital",
                    "status_code": 404
                }
            )

        associations = self.association_repository.get_by_public_acquisition(
            public_acquisition.id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.association_repository.get_by_public_acquisition_count(public_acquisition.id)

        return PaginatedResponse.create(
            items=associations,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET PUBLIC ACQUISITIONS BY ITEM]
    # [Lista todas as licitações que contêm um item com paginação]
    # [ENTRADA: item_id, pagination, hospital_id]
    # [SAIDA: PaginatedResponse[ItemPublicAcquisition]]
    # [DEPENDENCIAS: repositories]
    def get_public_acquisitions_by_item(
        self, item_id: UUID, pagination: PaginationParams, hospital_id: int
    ) -> PaginatedResponse[ItemPublicAcquisition]:
        # Validate item exists and belongs to hospital
        item = self.item_repository.get_by_public_id(item_id, hospital_id)
        if not item:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Item with ID '{item_id}' not found in this hospital",
                    "status_code": 404
                }
            )

        associations = self.association_repository.get_by_item(
            item.id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.association_repository.get_by_item_count(item.id)

        return PaginatedResponse.create(
            items=associations,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE ASSOCIATION]
    # [Atualiza fornecedor e/ou is_holder de uma associação]
    # [ENTRADA: public_id, association_data, hospital_id]
    # [SAIDA: ItemPublicAcquisition ou HTTPException]
    # [DEPENDENCIAS: repositories]
    def update_association(
        self, public_id: UUID, association_data: ItemPublicAcquisitionUpdate, hospital_id: int
    ) -> ItemPublicAcquisition:
        association = self.association_repository.get_by_public_id(public_id)
        if not association:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Association with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        supplier_internal_id = None
        # Validate new supplier if provided
        if association_data.supplier_id:
            supplier = self.supplier_repository.get_by_public_id(association_data.supplier_id, hospital_id)
            if not supplier:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"Supplier with ID '{association_data.supplier_id}' not found in this hospital",
                        "status_code": 404
                    }
                )
            supplier_internal_id = supplier.id

        return self.association_repository.update(
            association,
            supplier_internal_id,
            association_data.is_holder
        )

    # [DELETE ASSOCIATION]
    # [Remove associação (desassocia item da licitação)]
    # [ENTRADA: public_id]
    # [SAIDA: None ou HTTPException]
    # [DEPENDENCIAS: association_repository]
    def delete_association(self, public_id: UUID) -> None:
        association = self.association_repository.get_by_public_id(public_id)
        if not association:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Association with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        self.association_repository.delete(association)

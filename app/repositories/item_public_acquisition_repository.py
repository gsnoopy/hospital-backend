from sqlalchemy.orm import Session
from app.models.item_public_acquisition import ItemPublicAcquisition
from app.schemas.item_public_acquisition import ItemPublicAcquisitionCreate, ItemPublicAcquisitionUpdate
from typing import Optional, List
from uuid import UUID


# [ITEM PUBLIC ACQUISITION REPOSITORY]
# [Repository para operações CRUD da entidade ItemPublicAcquisition no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância ItemPublicAcquisitionRepository configurada]
# [DEPENDENCIAS: Session]
class ItemPublicAcquisitionRepository:

    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE]
    # [Cria uma nova associação item-licitação-fornecedor no banco de dados]
    # [ENTRADA: item_internal_id, public_acquisition_internal_id, supplier_internal_id, is_holder]
    # [SAIDA: ItemPublicAcquisition - instância da associação criada]
    # [DEPENDENCIAS: ItemPublicAcquisition, self.db]
    def create(self, item_internal_id: int, public_acquisition_internal_id: int, supplier_internal_id: int, is_holder: bool = False) -> ItemPublicAcquisition:
        db_association = ItemPublicAcquisition(
            item_id=item_internal_id,
            public_acquisition_id=public_acquisition_internal_id,
            supplier_id=supplier_internal_id,
            is_holder=is_holder,
        )
        self.db.add(db_association)
        self.db.commit()
        self.db.refresh(db_association)
        return db_association

    # [GET BY PUBLIC ID]
    # [Busca uma associação pelo UUID público]
    # [ENTRADA: public_id - UUID público da associação]
    # [SAIDA: Optional[ItemPublicAcquisition] - associação encontrada ou None]
    # [DEPENDENCIAS: ItemPublicAcquisition, self.db]
    def get_by_public_id(self, public_id: UUID) -> Optional[ItemPublicAcquisition]:
        return self.db.query(ItemPublicAcquisition).filter(
            ItemPublicAcquisition.public_id == public_id
        ).first()

    # [GET BY ITEM AND PUBLIC ACQUISITION]
    # [Busca associação específica entre item e licitação]
    # [ENTRADA: item_id, public_acquisition_id - IDs internos]
    # [SAIDA: Optional[ItemPublicAcquisition]]
    # [DEPENDENCIAS: ItemPublicAcquisition, self.db]
    def get_by_item_and_public_acquisition(self, item_id: int, public_acquisition_id: int) -> Optional[ItemPublicAcquisition]:
        return self.db.query(ItemPublicAcquisition).filter(
            ItemPublicAcquisition.item_id == item_id,
            ItemPublicAcquisition.public_acquisition_id == public_acquisition_id
        ).first()

    # [GET BY PUBLIC ACQUISITION]
    # [Busca todas as associações (itens) de uma licitação com paginação]
    # [ENTRADA: public_acquisition_id - ID interno da licitação, skip, limit]
    # [SAIDA: List[ItemPublicAcquisition]]
    # [DEPENDENCIAS: ItemPublicAcquisition, self.db]
    def get_by_public_acquisition(self, public_acquisition_id: int, skip: int = 0, limit: int = 100) -> List[ItemPublicAcquisition]:
        return self.db.query(ItemPublicAcquisition).filter(
            ItemPublicAcquisition.public_acquisition_id == public_acquisition_id
        ).offset(skip).limit(limit).all()

    # [GET BY PUBLIC ACQUISITION COUNT]
    # [Conta total de itens em uma licitação]
    # [ENTRADA: public_acquisition_id - ID interno da licitação]
    # [SAIDA: int - número total de itens]
    # [DEPENDENCIAS: ItemPublicAcquisition, self.db]
    def get_by_public_acquisition_count(self, public_acquisition_id: int) -> int:
        return self.db.query(ItemPublicAcquisition).filter(
            ItemPublicAcquisition.public_acquisition_id == public_acquisition_id
        ).count()

    # [GET BY ITEM]
    # [Busca todas as licitações que contêm um item com paginação]
    # [ENTRADA: item_id - ID interno do item, skip, limit]
    # [SAIDA: List[ItemPublicAcquisition]]
    # [DEPENDENCIAS: ItemPublicAcquisition, self.db]
    def get_by_item(self, item_id: int, skip: int = 0, limit: int = 100) -> List[ItemPublicAcquisition]:
        return self.db.query(ItemPublicAcquisition).filter(
            ItemPublicAcquisition.item_id == item_id
        ).offset(skip).limit(limit).all()

    # [GET BY ITEM COUNT]
    # [Conta total de licitações que contêm um item]
    # [ENTRADA: item_id - ID interno do item]
    # [SAIDA: int - número total de licitações]
    # [DEPENDENCIAS: ItemPublicAcquisition, self.db]
    def get_by_item_count(self, item_id: int) -> int:
        return self.db.query(ItemPublicAcquisition).filter(
            ItemPublicAcquisition.item_id == item_id
        ).count()

    # [UPDATE]
    # [Atualiza uma associação existente (fornecedor e/ou is_holder)]
    # [ENTRADA: association - instância da associação, supplier_internal_id - novo ID do fornecedor (opcional), is_holder - status holder (opcional)]
    # [SAIDA: ItemPublicAcquisition - associação atualizada]
    # [DEPENDENCIAS: self.db]
    def update(self, association: ItemPublicAcquisition, supplier_internal_id: Optional[int] = None, is_holder: Optional[bool] = None) -> ItemPublicAcquisition:
        if supplier_internal_id is not None:
            association.supplier_id = supplier_internal_id
        if is_holder is not None:
            association.is_holder = is_holder
        self.db.commit()
        self.db.refresh(association)
        return association

    # [DELETE]
    # [Remove uma associação do banco (desassocia item da licitação)]
    # [ENTRADA: association - instância da associação a ser removida]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, association: ItemPublicAcquisition) -> None:
        self.db.delete(association)
        self.db.commit()

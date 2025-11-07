from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.models.items import Item
from app.schemas.items import ItemCreate, ItemUpdate
from typing import Optional, List
from uuid import UUID


# [ITEM REPOSITORY]
# [Repository para operações CRUD da entidade Item no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância ItemRepository configurada]
# [DEPENDENCIAS: Session]
class ItemRepository:

    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE ITEM]
    # [Cria um novo item no banco de dados]
    # [ENTRADA: item_data - dados do item via schema, subcategory_internal_id - ID interno da subcategoria, hospital_internal_id - ID interno do hospital]
    # [SAIDA: Item - instância do item criado com relacionamentos carregados]
    # [DEPENDENCIAS: Item, self.db, joinedload]
    def create(self, item_data: ItemCreate, subcategory_internal_id: int, hospital_internal_id: int) -> Item:
        db_item = Item(
            name=item_data.name,
            similar_names=item_data.similar_names,
            description=item_data.description,
            full_description=item_data.full_description,
            internal_code=item_data.internal_code,
            presentation=item_data.presentation,
            sample=item_data.sample,
            has_catalog=item_data.has_catalog,
            subcategory_id=subcategory_internal_id,
            hospital_id=hospital_internal_id,
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    # [GET BY PUBLIC ID]
    # [Busca um item pelo UUID público filtrando por hospital]
    # [ENTRADA: public_id - UUID público do item, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[Item] - item encontrado ou None]
    # [DEPENDENCIAS: Item, self.db]
    def get_by_public_id(self, public_id: UUID, hospital_id: int) -> Optional[Item]:
        return self.db.query(Item).filter(
            Item.public_id == public_id,
            Item.hospital_id == hospital_id
        ).first()

    # [GET BY INTERNAL CODE]
    # [Busca um item pelo código interno único dentro de um hospital]
    # [ENTRADA: internal_code - código interno do item, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[Item] - item encontrado ou None]
    # [DEPENDENCIAS: Item, self.db]
    def get_by_internal_code(self, internal_code: str, hospital_id: int) -> Optional[Item]:
        return self.db.query(Item).filter(
            Item.internal_code == internal_code,
            Item.hospital_id == hospital_id
        ).first()

    # [GET ALL]
    # [Busca todos os itens de um hospital com paginação]
    # [ENTRADA: hospital_id - ID interno do hospital, skip - registros a pular, limit - limite de registros]
    # [SAIDA: List[Item] - lista de itens]
    # [DEPENDENCIAS: Item, self.db]
    def get_all(self, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).filter(
            Item.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET TOTAL COUNT]
    # [Conta total de itens de um hospital]
    # [ENTRADA: hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de itens]
    # [DEPENDENCIAS: Item, self.db]
    def get_total_count(self, hospital_id: int) -> int:
        return self.db.query(Item).filter(Item.hospital_id == hospital_id).count()

    # [GET BY SUBCATEGORY ID]
    # [Busca itens por subcategoria e hospital com paginação]
    # [ENTRADA: subcategory_id - ID interno da subcategoria, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[Item] - lista de itens da subcategoria]
    # [DEPENDENCIAS: Item, self.db]
    def get_by_subcategory_id(self, subcategory_id: int, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).filter(
            Item.subcategory_id == subcategory_id,
            Item.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET SUBCATEGORY COUNT]
    # [Conta total de itens em uma subcategoria de um hospital]
    # [ENTRADA: subcategory_id - ID interno da subcategoria, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de itens]
    # [DEPENDENCIAS: Item, self.db]
    def get_subcategory_count(self, subcategory_id: int, hospital_id: int) -> int:
        return self.db.query(Item).filter(
            Item.subcategory_id == subcategory_id,
            Item.hospital_id == hospital_id
        ).count()

    # [SEARCH BY NAME]
    # [Busca itens por nome (busca parcial) filtrando por hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[Item] - lista de itens que contêm o termo]
    # [DEPENDENCIAS: Item, self.db]
    def search_by_name(self, search_term: str, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).filter(
            Item.name.ilike(f"%{search_term}%"),
            Item.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET SEARCH COUNT]
    # [Conta total de itens que contêm termo de busca em um hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de itens encontrados]
    # [DEPENDENCIAS: Item, self.db]
    def get_search_count(self, search_term: str, hospital_id: int) -> int:
        return self.db.query(Item).filter(
            Item.name.ilike(f"%{search_term}%"),
            Item.hospital_id == hospital_id
        ).count()

    # [SEARCH BY SIMILAR NAMES]
    # [Busca itens por similar_names (array de strings) filtrando por hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[Item] - lista de itens com similar_names contendo o termo]
    # [DEPENDENCIAS: Item, self.db, func]
    def search_by_similar_names(self, search_term: str, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).filter(
            func.array_to_string(Item.similar_names, ' ').ilike(f"%{search_term}%"),
            Item.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET SIMILAR NAMES SEARCH COUNT]
    # [Conta total de itens com similar_names contendo o termo em um hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de itens encontrados]
    # [DEPENDENCIAS: Item, self.db, func]
    def get_similar_names_search_count(self, search_term: str, hospital_id: int) -> int:
        return self.db.query(Item).filter(
            func.array_to_string(Item.similar_names, ' ').ilike(f"%{search_term}%"),
            Item.hospital_id == hospital_id
        ).count()

    # [SEARCH UNIFIED]
    # [Busca unificada em name E similar_names usando OR]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[Item] - lista de itens encontrados em name OU similar_names]
    # [DEPENDENCIAS: Item, self.db, or_, func]
    def search_unified(self, search_term: str, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        return self.db.query(Item).filter(
            or_(
                Item.name.ilike(f"%{search_term}%"),
                func.array_to_string(Item.similar_names, ' ').ilike(f"%{search_term}%")
            ),
            Item.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET UNIFIED SEARCH COUNT]
    # [Conta total de itens encontrados em name OU similar_names]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de itens encontrados]
    # [DEPENDENCIAS: Item, self.db, or_, func]
    def get_unified_search_count(self, search_term: str, hospital_id: int) -> int:
        return self.db.query(Item).filter(
            or_(
                Item.name.ilike(f"%{search_term}%"),
                func.array_to_string(Item.similar_names, ' ').ilike(f"%{search_term}%")
            ),
            Item.hospital_id == hospital_id
        ).count()

    # [UPDATE ITEM]
    # [Atualiza um item existente]
    # [ENTRADA: item - instância do item, item_data - novos dados, subcategory_internal_id - ID interno da subcategoria]
    # [SAIDA: Item - item atualizado]
    # [DEPENDENCIAS: self.db]
    def update(self, item: Item, item_data: ItemUpdate, subcategory_internal_id: Optional[int] = None) -> Item:
        update_data = item_data.model_dump(exclude_unset=True, exclude={'subcategory_id'})
        for field, value in update_data.items():
            setattr(item, field, value)

        if subcategory_internal_id is not None:
            item.subcategory_id = subcategory_internal_id

        self.db.commit()
        self.db.refresh(item)
        return item

    # [DELETE ITEM]
    # [Remove um item do banco (hard delete)]
    # [ENTRADA: item - instância do item a ser removido]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, item: Item) -> None:
        self.db.delete(item)
        self.db.commit()

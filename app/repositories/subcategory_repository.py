from sqlalchemy.orm import Session, joinedload
from app.models.subcategories import SubCategory
from app.schemas.subcategory import SubCategoryCreate, SubCategoryUpdate
from typing import Optional, List
from uuid import UUID


# [SUBCATEGORY REPOSITORY]
# [Repository para operações CRUD da entidade SubCategory no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância SubCategoryRepository configurada]
# [DEPENDENCIAS: Session]
class SubCategoryRepository:

    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE SUBCATEGORY]
    # [Cria uma nova subcategoria no banco de dados]
    # [ENTRADA: subcategory_data - dados da subcategoria via schema, category_internal_id - ID interno da categoria, hospital_internal_id - ID interno do hospital]
    # [SAIDA: SubCategory - instância da subcategoria criada com relacionamentos]
    # [DEPENDENCIAS: SubCategory, self.db, joinedload]
    def create(self, subcategory_data: SubCategoryCreate, category_internal_id: int, hospital_internal_id: int) -> SubCategory:
        db_subcategory = SubCategory(
            name=subcategory_data.name,
            description=subcategory_data.description,
            category_id=category_internal_id,
            hospital_id=hospital_internal_id,
        )
        self.db.add(db_subcategory)
        self.db.commit()
        self.db.refresh(db_subcategory)
        # Load relationships
        db_subcategory = self.db.query(SubCategory).options(
            joinedload(SubCategory.category),
            joinedload(SubCategory.hospital)
        ).filter(SubCategory.id == db_subcategory.id).first()
        return db_subcategory

    # [GET BY PUBLIC ID]
    # [Busca uma subcategoria pelo UUID público com relacionamentos]
    # [ENTRADA: public_id - UUID público da subcategoria, hospital_id - ID interno do hospital (opcional para filtro)]
    # [SAIDA: Optional[SubCategory] - subcategoria encontrada ou None]
    # [DEPENDENCIAS: SubCategory, self.db, joinedload]
    def get_by_public_id(self, public_id: UUID, hospital_id: Optional[int] = None) -> Optional[SubCategory]:
        query = self.db.query(SubCategory).options(
            joinedload(SubCategory.category),
            joinedload(SubCategory.hospital)
        ).filter(SubCategory.public_id == public_id)

        if hospital_id:
            query = query.filter(SubCategory.hospital_id == hospital_id)

        return query.first()

    # [GET BY NAME]
    # [Busca uma subcategoria pelo nome e hospital]
    # [ENTRADA: name - nome da subcategoria, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[SubCategory] - subcategoria encontrada ou None]
    # [DEPENDENCIAS: SubCategory, self.db, joinedload]
    def get_by_name(self, name: str, hospital_id: int) -> Optional[SubCategory]:
        return self.db.query(SubCategory).options(
            joinedload(SubCategory.category),
            joinedload(SubCategory.hospital)
        ).filter(
            SubCategory.name == name,
            SubCategory.hospital_id == hospital_id
        ).first()

    # [GET BY CATEGORY]
    # [Busca subcategorias por categoria e hospital]
    # [ENTRADA: category_id - ID interno da categoria, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[SubCategory] - lista de subcategorias da categoria]
    # [DEPENDENCIAS: SubCategory, self.db, joinedload]
    def get_by_category(self, category_id: int, hospital_id: int, skip: int = 0, limit: int = 100) -> List[SubCategory]:
        return self.db.query(SubCategory).options(
            joinedload(SubCategory.category),
            joinedload(SubCategory.hospital)
        ).filter(
            SubCategory.category_id == category_id,
            SubCategory.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET ALL]
    # [Busca todas as subcategorias de um hospital com paginação]
    # [ENTRADA: hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[SubCategory] - lista de subcategorias do hospital]
    # [DEPENDENCIAS: SubCategory, self.db, joinedload]
    def get_all(self, hospital_id: int, skip: int = 0, limit: int = 100) -> List[SubCategory]:
        return self.db.query(SubCategory).options(
            joinedload(SubCategory.category),
            joinedload(SubCategory.hospital)
        ).filter(SubCategory.hospital_id == hospital_id).offset(skip).limit(limit).all()

    # [GET TOTAL COUNT]
    # [Conta total de subcategorias de um hospital]
    # [ENTRADA: hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de subcategorias]
    # [DEPENDENCIAS: SubCategory, self.db]
    def get_total_count(self, hospital_id: int) -> int:
        return self.db.query(SubCategory).filter(SubCategory.hospital_id == hospital_id).count()

    # [GET TOTAL COUNT BY CATEGORY]
    # [Conta total de subcategorias ativas por categoria e hospital]
    # [ENTRADA: category_id - ID interno da categoria, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de subcategorias da categoria]
    # [DEPENDENCIAS: SubCategory, self.db]
    def get_total_count_by_category(self, category_id: int, hospital_id: int) -> int:
        return self.db.query(SubCategory).filter(
            SubCategory.category_id == category_id,
            SubCategory.hospital_id == hospital_id
        ).count()

    # [UPDATE SUBCATEGORY]
    # [Atualiza uma subcategoria existente]
    # [ENTRADA: subcategory - instância da subcategoria, subcategory_data - novos dados, category_internal_id - novo ID da categoria (opcional)]
    # [SAIDA: SubCategory - subcategoria atualizada com relacionamentos carregados]
    # [DEPENDENCIAS: self.db, joinedload]
    def update(self, subcategory: SubCategory, subcategory_data: SubCategoryUpdate, category_internal_id: Optional[int] = None) -> SubCategory:
        update_data = subcategory_data.model_dump(exclude_unset=True, exclude={'category_id'})
        for field, value in update_data.items():
            setattr(subcategory, field, value)

        if category_internal_id is not None:
            subcategory.category_id = category_internal_id

        self.db.commit()
        self.db.refresh(subcategory)
        # Reload with relationships
        subcategory = self.db.query(SubCategory).options(
            joinedload(SubCategory.category),
            joinedload(SubCategory.hospital)
        ).filter(SubCategory.id == subcategory.id).first()
        return subcategory

    # [DELETE SUBCATEGORY]
    # [Remove uma subcategoria do banco (soft delete)]
    # [ENTRADA: subcategory - instância da subcategoria a ser removida]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, subcategory: SubCategory) -> None:
        self.db.delete(subcategory)
        self.db.commit()
from sqlalchemy.orm import Session, joinedload
from app.models.categories import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from typing import Optional, List
from uuid import UUID


# [CATEGORY REPOSITORY]
# [Repository para operações CRUD da entidade Category no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância CategoryRepository configurada]
# [DEPENDENCIAS: Session]
class CategoryRepository:

    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE CATEGORY]
    # [Cria uma nova categoria no banco de dados]
    # [ENTRADA: category_data - dados da categoria via schema, hospital_internal_id - ID interno do hospital]
    # [SAIDA: Category - instância da categoria criada com relacionamentos carregados]
    # [DEPENDENCIAS: Category, self.db, joinedload]
    def create(self, category_data: CategoryCreate, hospital_internal_id: int) -> Category:
        db_category = Category(
            name=category_data.name,
            description=category_data.description,
            hospital_id=hospital_internal_id,
        )
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        # Load relationships
        db_category = self.db.query(Category).options(
            joinedload(Category.hospital)
        ).filter(Category.id == db_category.id).first()
        return db_category

    # [GET BY PUBLIC ID]
    # [Busca uma categoria pelo UUID público com relacionamentos]
    # [ENTRADA: public_id - UUID público da categoria, hospital_id - ID interno do hospital (opcional para filtro)]
    # [SAIDA: Optional[Category] - categoria encontrada ou None]
    # [DEPENDENCIAS: Category, self.db, joinedload]
    def get_by_public_id(self, public_id: UUID, hospital_id: Optional[int] = None) -> Optional[Category]:
        query = self.db.query(Category).options(
            joinedload(Category.hospital)
        ).filter(Category.public_id == public_id)

        if hospital_id:
            query = query.filter(Category.hospital_id == hospital_id)

        return query.first()

    # [GET BY NAME]
    # [Busca uma categoria pelo nome e hospital]
    # [ENTRADA: name - nome da categoria, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[Category] - categoria encontrada ou None]
    # [DEPENDENCIAS: Category, self.db]
    def get_by_name(self, name: str, hospital_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(
            Category.name == name,
            Category.hospital_id == hospital_id
        ).first()

    # [GET ALL]
    # [Busca todas as categorias de um hospital com paginação]
    # [ENTRADA: hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[Category] - lista de categorias do hospital]
    # [DEPENDENCIAS: Category, self.db, joinedload]
    def get_all(self, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.db.query(Category).options(
            joinedload(Category.hospital)
        ).filter(Category.hospital_id == hospital_id).offset(skip).limit(limit).all()

    # [GET ALL WITH SUBCATEGORIES]
    # [Busca todas as categorias de um hospital com suas subcategorias aninhadas]
    # [ENTRADA: hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[Category] - lista de categorias do hospital com subcategorias]
    # [DEPENDENCIAS: Category, self.db, joinedload]
    def get_all_with_subcategories(self, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.db.query(Category).options(
            joinedload(Category.hospital),
            joinedload(Category.subcategories)
        ).filter(Category.hospital_id == hospital_id).offset(skip).limit(limit).all()

    # [GET TOTAL COUNT]
    # [Conta total de categorias de um hospital]
    # [ENTRADA: hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de categorias]
    # [DEPENDENCIAS: Category, self.db]
    def get_total_count(self, hospital_id: int) -> int:
        return self.db.query(Category).filter(Category.hospital_id == hospital_id).count()

    # [UPDATE CATEGORY]
    # [Atualiza uma categoria existente]
    # [ENTRADA: category - instância da categoria, category_data - novos dados]
    # [SAIDA: Category - categoria atualizada com relacionamentos carregados]
    # [DEPENDENCIAS: self.db, joinedload]
    def update(self, category: Category, category_data: CategoryUpdate) -> Category:
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)

        category = self.db.query(Category).options(
            joinedload(Category.hospital)
        ).filter(Category.id == category.id).first()
        return category

    # [DELETE CATEGORY]
    # [Remove uma categoria do banco (soft delete)]
    # [ENTRADA: category - instância da categoria a ser removida]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()
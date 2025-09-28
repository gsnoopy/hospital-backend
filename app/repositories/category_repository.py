from sqlalchemy.orm import Session
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
    # [ENTRADA: category_data - dados da categoria via schema]
    # [SAIDA: Category - instância da categoria criada]
    # [DEPENDENCIAS: Category, self.db]
    def create(self, category_data: CategoryCreate) -> Category:
        db_category = Category(
            name=category_data.name,
            description=category_data.description,
        )
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    # [GET BY PUBLIC ID]
    # [Busca uma categoria pelo UUID público]
    # [ENTRADA: public_id - UUID público da categoria]
    # [SAIDA: Optional[Category] - categoria encontrada ou None]
    # [DEPENDENCIAS: Category, self.db]
    def get_by_public_id(self, public_id: UUID) -> Optional[Category]:
        return self.db.query(Category).filter(Category.public_id == public_id).first()

    # [GET BY NAME]
    # [Busca uma categoria pelo nome]
    # [ENTRADA: name - nome da categoria]
    # [SAIDA: Optional[Category] - categoria encontrada ou None]
    # [DEPENDENCIAS: Category, self.db]
    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()

    # [GET ALL]
    # [Busca todas as categorias com paginação]
    # [ENTRADA: skip - registros a pular, limit - limite de registros]
    # [SAIDA: List[Category] - lista de categorias]
    # [DEPENDENCIAS: Category, self.db]
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.db.query(Category).offset(skip).limit(limit).all()

    # [GET TOTAL COUNT]
    # [Conta total de categorias ativas]
    # [ENTRADA: nenhuma]
    # [SAIDA: int - número total de categorias]
    # [DEPENDENCIAS: Category, self.db]
    def get_total_count(self) -> int:
        return self.db.query(Category).count()

    # [UPDATE CATEGORY]
    # [Atualiza uma categoria existente]
    # [ENTRADA: category - instância da categoria, category_data - novos dados]
    # [SAIDA: Category - categoria atualizada]
    # [DEPENDENCIAS: self.db]
    def update(self, category: Category, category_data: CategoryUpdate) -> Category:
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)
        return category

    # [DELETE CATEGORY]
    # [Remove uma categoria do banco (soft delete)]
    # [ENTRADA: category - instância da categoria a ser removida]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()
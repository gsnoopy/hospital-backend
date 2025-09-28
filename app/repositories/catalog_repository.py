from sqlalchemy.orm import Session
from app.models.catalog import Catalog
from app.schemas.catalog import CatalogCreate, CatalogUpdate
from typing import Optional, List
from uuid import UUID


# [CATALOG REPOSITORY]
# [Repository para operações CRUD da entidade Catalog no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância CatalogRepository configurada]
# [DEPENDENCIAS: Session]
class CatalogRepository:

    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE CATALOG]
    # [Cria um novo item de catálogo no banco de dados]
    # [ENTRADA: catalog_data - dados do catálogo via schema]
    # [SAIDA: Catalog - instância do catálogo criado]
    # [DEPENDENCIAS: Catalog, self.db]
    def create(self, catalog_data: CatalogCreate) -> Catalog:
        db_catalog = Catalog(
            name=catalog_data.name,
            description=catalog_data.description,
            full_description=catalog_data.full_description,
            presentation=catalog_data.presentation,
        )
        self.db.add(db_catalog)
        self.db.commit()
        self.db.refresh(db_catalog)
        return db_catalog

    # [GET BY PUBLIC ID]
    # [Busca um catálogo pelo UUID público]
    # [ENTRADA: public_id - UUID público do catálogo]
    # [SAIDA: Optional[Catalog] - catálogo encontrado ou None]
    # [DEPENDENCIAS: Catalog, self.db]
    def get_by_public_id(self, public_id: UUID) -> Optional[Catalog]:
        return self.db.query(Catalog).filter(Catalog.public_id == public_id).first()

    # [GET BY NAME]
    # [Busca um catálogo pelo nome]
    # [ENTRADA: name - nome do catálogo]
    # [SAIDA: Optional[Catalog] - catálogo encontrado ou None]
    # [DEPENDENCIAS: Catalog, self.db]
    def get_by_name(self, name: str) -> Optional[Catalog]:
        return self.db.query(Catalog).filter(Catalog.name == name).first()

    # [GET ALL]
    # [Busca todos os catálogos com paginação]
    # [ENTRADA: skip - registros a pular, limit - limite de registros]
    # [SAIDA: List[Catalog] - lista de catálogos]
    # [DEPENDENCIAS: Catalog, self.db]
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Catalog]:
        return self.db.query(Catalog).offset(skip).limit(limit).all()

    # [GET TOTAL COUNT]
    # [Conta total de catálogos]
    # [ENTRADA: nenhuma]
    # [SAIDA: int - número total de catálogos]
    # [DEPENDENCIAS: Catalog, self.db]
    def get_total_count(self) -> int:
        return self.db.query(Catalog).count()

    # [SEARCH BY NAME]
    # [Busca catálogos por nome (busca parcial)]
    # [ENTRADA: search_term - termo de busca, skip - registros a pular, limit - limite]
    # [SAIDA: List[Catalog] - lista de catálogos que contêm o termo]
    # [DEPENDENCIAS: Catalog, self.db]
    def search_by_name(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Catalog]:
        return self.db.query(Catalog).filter(
            Catalog.name.ilike(f"%{search_term}%")
        ).offset(skip).limit(limit).all()

    # [GET SEARCH COUNT]
    # [Conta total de catálogos que contêm termo de busca]
    # [ENTRADA: search_term - termo de busca]
    # [SAIDA: int - número total de catálogos encontrados]
    # [DEPENDENCIAS: Catalog, self.db]
    def get_search_count(self, search_term: str) -> int:
        return self.db.query(Catalog).filter(
            Catalog.name.ilike(f"%{search_term}%")
        ).count()

    # [UPDATE CATALOG]
    # [Atualiza um catálogo existente]
    # [ENTRADA: catalog - instância do catálogo, catalog_data - novos dados]
    # [SAIDA: Catalog - catálogo atualizado]
    # [DEPENDENCIAS: self.db]
    def update(self, catalog: Catalog, catalog_data: CatalogUpdate) -> Catalog:
        update_data = catalog_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(catalog, field, value)

        self.db.commit()
        self.db.refresh(catalog)
        return catalog

    # [DELETE CATALOG]
    # [Remove um catálogo do banco (hard delete)]
    # [ENTRADA: catalog - instância do catálogo a ser removido]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, catalog: Catalog) -> None:
        self.db.delete(catalog)
        self.db.commit()
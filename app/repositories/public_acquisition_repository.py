from sqlalchemy.orm import Session
from app.models.public_acquisition import PublicAcquisition
from app.schemas.public_acquisition import PublicAcquisitionCreate, PublicAcquisitionUpdate
from typing import Optional, List
from uuid import UUID


# [PUBLIC ACQUISITION REPOSITORY]
# [Repository para operações CRUD da entidade PublicAcquisition no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância PublicAcquisitionRepository configurada]
# [DEPENDENCIAS: Session]
class PublicAcquisitionRepository:

    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE PUBLIC ACQUISITION]
    # [Cria uma nova licitação pública no banco de dados]
    # [ENTRADA: public_acquisition_data - dados da licitação via schema, hospital_internal_id - ID interno do hospital, user_internal_id - ID interno do usuário Pregoeiro]
    # [SAIDA: PublicAcquisition - instância da licitação criada]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def create(self, public_acquisition_data: PublicAcquisitionCreate, hospital_internal_id: int, user_internal_id: int) -> PublicAcquisition:
        db_public_acquisition = PublicAcquisition(
            code=public_acquisition_data.code,
            title=public_acquisition_data.title,
            year=public_acquisition_data.year,
            hospital_id=hospital_internal_id,
            user_id=user_internal_id,
        )
        self.db.add(db_public_acquisition)
        self.db.commit()
        self.db.refresh(db_public_acquisition)
        return db_public_acquisition

    # [GET BY PUBLIC ID]
    # [Busca uma licitação pelo UUID público filtrando por hospital]
    # [ENTRADA: public_id - UUID público da licitação, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[PublicAcquisition] - licitação encontrada ou None]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def get_by_public_id(self, public_id: UUID, hospital_id: int) -> Optional[PublicAcquisition]:
        return self.db.query(PublicAcquisition).filter(
            PublicAcquisition.public_id == public_id,
            PublicAcquisition.hospital_id == hospital_id
        ).first()

    # [GET BY CODE]
    # [Busca uma licitação pelo código dentro de um hospital]
    # [ENTRADA: code - código da licitação, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[PublicAcquisition] - licitação encontrada ou None]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def get_by_code(self, code: str, hospital_id: int) -> Optional[PublicAcquisition]:
        return self.db.query(PublicAcquisition).filter(
            PublicAcquisition.code == code,
            PublicAcquisition.hospital_id == hospital_id
        ).first()

    # [GET ALL]
    # [Busca todas as licitações de um hospital com paginação]
    # [ENTRADA: hospital_id - ID interno do hospital, skip - registros a pular, limit - limite de registros]
    # [SAIDA: List[PublicAcquisition] - lista de licitações]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def get_all(self, hospital_id: int, skip: int = 0, limit: int = 100) -> List[PublicAcquisition]:
        return self.db.query(PublicAcquisition).filter(
            PublicAcquisition.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET TOTAL COUNT]
    # [Conta total de licitações de um hospital]
    # [ENTRADA: hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de licitações]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def get_total_count(self, hospital_id: int) -> int:
        return self.db.query(PublicAcquisition).filter(PublicAcquisition.hospital_id == hospital_id).count()

    # [SEARCH BY TITLE]
    # [Busca licitações por título (busca parcial) filtrando por hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[PublicAcquisition] - lista de licitações que contêm o termo]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def search_by_title(self, search_term: str, hospital_id: int, skip: int = 0, limit: int = 100) -> List[PublicAcquisition]:
        return self.db.query(PublicAcquisition).filter(
            PublicAcquisition.title.ilike(f"%{search_term}%"),
            PublicAcquisition.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET SEARCH COUNT]
    # [Conta total de licitações que contêm termo de busca em um hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de licitações encontradas]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def get_search_count(self, search_term: str, hospital_id: int) -> int:
        return self.db.query(PublicAcquisition).filter(
            PublicAcquisition.title.ilike(f"%{search_term}%"),
            PublicAcquisition.hospital_id == hospital_id
        ).count()

    # [SEARCH BY CODE]
    # [Busca licitações por código (busca parcial) filtrando por hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[PublicAcquisition] - lista de licitações que contêm o termo]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def search_by_code(self, search_term: str, hospital_id: int, skip: int = 0, limit: int = 100) -> List[PublicAcquisition]:
        return self.db.query(PublicAcquisition).filter(
            PublicAcquisition.code.ilike(f"%{search_term}%"),
            PublicAcquisition.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET CODE SEARCH COUNT]
    # [Conta total de licitações que contêm termo de busca no código em um hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de licitações encontradas]
    # [DEPENDENCIAS: PublicAcquisition, self.db]
    def get_code_search_count(self, search_term: str, hospital_id: int) -> int:
        return self.db.query(PublicAcquisition).filter(
            PublicAcquisition.code.ilike(f"%{search_term}%"),
            PublicAcquisition.hospital_id == hospital_id
        ).count()

    # [UPDATE PUBLIC ACQUISITION]
    # [Atualiza uma licitação existente]
    # [ENTRADA: public_acquisition - instância da licitação, public_acquisition_data - novos dados]
    # [SAIDA: PublicAcquisition - licitação atualizada]
    # [DEPENDENCIAS: self.db]
    def update(self, public_acquisition: PublicAcquisition, public_acquisition_data: PublicAcquisitionUpdate) -> PublicAcquisition:
        update_data = public_acquisition_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(public_acquisition, field, value)

        self.db.commit()
        self.db.refresh(public_acquisition)
        return public_acquisition

    # [DELETE PUBLIC ACQUISITION]
    # [Remove uma licitação do banco (hard delete)]
    # [ENTRADA: public_acquisition - instância da licitação a ser removida]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, public_acquisition: PublicAcquisition) -> None:
        self.db.delete(public_acquisition)
        self.db.commit()

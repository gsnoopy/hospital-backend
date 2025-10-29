from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from typing import Optional, List
from uuid import UUID


# [SUPPLIER REPOSITORY]
# [Repository para operações CRUD da entidade Supplier no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância SupplierRepository configurada]
# [DEPENDENCIAS: Session]
class SupplierRepository:

    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE SUPPLIER]
    # [Cria um novo fornecedor no banco de dados]
    # [ENTRADA: supplier_data - dados do fornecedor via schema, hospital_internal_id - ID interno do hospital]
    # [SAIDA: Supplier - instância do fornecedor criado]
    # [DEPENDENCIAS: Supplier, self.db]
    def create(self, supplier_data: SupplierCreate, hospital_internal_id: int) -> Supplier:
        db_supplier = Supplier(
            name=supplier_data.name,
            document_type=supplier_data.document_type,
            document=supplier_data.document,
            email=supplier_data.email,
            phone=supplier_data.phone,
            hospital_id=hospital_internal_id,
        )
        self.db.add(db_supplier)
        self.db.commit()
        self.db.refresh(db_supplier)
        return db_supplier

    # [GET BY PUBLIC ID]
    # [Busca um fornecedor pelo UUID público filtrando por hospital]
    # [ENTRADA: public_id - UUID público do fornecedor, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[Supplier] - fornecedor encontrado ou None]
    # [DEPENDENCIAS: Supplier, self.db]
    def get_by_public_id(self, public_id: UUID, hospital_id: int) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(
            Supplier.public_id == public_id,
            Supplier.hospital_id == hospital_id
        ).first()

    # [GET BY DOCUMENT]
    # [Busca um fornecedor pelo documento dentro de um hospital]
    # [ENTRADA: document - documento do fornecedor, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[Supplier] - fornecedor encontrado ou None]
    # [DEPENDENCIAS: Supplier, self.db]
    def get_by_document(self, document: str, hospital_id: int) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(
            Supplier.document == document,
            Supplier.hospital_id == hospital_id
        ).first()

    # [GET BY EMAIL]
    # [Busca um fornecedor pelo email dentro de um hospital]
    # [ENTRADA: email - email do fornecedor, hospital_id - ID interno do hospital]
    # [SAIDA: Optional[Supplier] - fornecedor encontrado ou None]
    # [DEPENDENCIAS: Supplier, self.db]
    def get_by_email(self, email: str, hospital_id: int) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(
            Supplier.email == email,
            Supplier.hospital_id == hospital_id
        ).first()

    # [GET ALL]
    # [Busca todos os fornecedores de um hospital com paginação]
    # [ENTRADA: hospital_id - ID interno do hospital, skip - registros a pular, limit - limite de registros]
    # [SAIDA: List[Supplier] - lista de fornecedores]
    # [DEPENDENCIAS: Supplier, self.db]
    def get_all(self, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return self.db.query(Supplier).filter(
            Supplier.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET TOTAL COUNT]
    # [Conta total de fornecedores de um hospital]
    # [ENTRADA: hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de fornecedores]
    # [DEPENDENCIAS: Supplier, self.db]
    def get_total_count(self, hospital_id: int) -> int:
        return self.db.query(Supplier).filter(Supplier.hospital_id == hospital_id).count()

    # [SEARCH BY NAME]
    # [Busca fornecedores por nome (busca parcial) filtrando por hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital, skip - registros a pular, limit - limite]
    # [SAIDA: List[Supplier] - lista de fornecedores que contêm o termo]
    # [DEPENDENCIAS: Supplier, self.db]
    def search_by_name(self, search_term: str, hospital_id: int, skip: int = 0, limit: int = 100) -> List[Supplier]:
        return self.db.query(Supplier).filter(
            Supplier.name.ilike(f"%{search_term}%"),
            Supplier.hospital_id == hospital_id
        ).offset(skip).limit(limit).all()

    # [GET SEARCH COUNT]
    # [Conta total de fornecedores que contêm termo de busca em um hospital]
    # [ENTRADA: search_term - termo de busca, hospital_id - ID interno do hospital]
    # [SAIDA: int - número total de fornecedores encontrados]
    # [DEPENDENCIAS: Supplier, self.db]
    def get_search_count(self, search_term: str, hospital_id: int) -> int:
        return self.db.query(Supplier).filter(
            Supplier.name.ilike(f"%{search_term}%"),
            Supplier.hospital_id == hospital_id
        ).count()

    # [UPDATE SUPPLIER]
    # [Atualiza um fornecedor existente]
    # [ENTRADA: supplier - instância do fornecedor, supplier_data - novos dados]
    # [SAIDA: Supplier - fornecedor atualizado]
    # [DEPENDENCIAS: self.db]
    def update(self, supplier: Supplier, supplier_data: SupplierUpdate) -> Supplier:
        update_data = supplier_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(supplier, field, value)

        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    # [DELETE SUPPLIER]
    # [Remove um fornecedor do banco (hard delete)]
    # [ENTRADA: supplier - instância do fornecedor a ser removido]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, supplier: Supplier) -> None:
        self.db.delete(supplier)
        self.db.commit()

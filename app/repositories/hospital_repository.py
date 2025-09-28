from sqlalchemy.orm import Session
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate
from typing import Optional
from uuid import UUID

# [HOSPITAL REPOSITORY]
# [Repository para operações CRUD da entidade Hospital no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância HospitalRepository configurada]
# [DEPENDENCIAS: Session]
class HospitalRepository:
    
    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE HOSPITAL]
    # [Cria um novo hospital no banco de dados]
    # [ENTRADA: hospital_data - dados do hospital via schema]
    # [SAIDA: Hospital - instância do hospital criado]
    # [DEPENDENCIAS: Hospital, self.db]
    def create(self, hospital_data: HospitalCreate) -> Hospital:
        db_hospital = Hospital(
            name=hospital_data.name,
            nationality=hospital_data.nationality,
            document_type=hospital_data.document_type,
            document=hospital_data.document,
            email=hospital_data.email,
            phone=hospital_data.phone,
            city=hospital_data.city,
        )
        self.db.add(db_hospital)
        self.db.commit()
        self.db.refresh(db_hospital)
        return db_hospital

    # [GET HOSPITAL BY ID]
    # [Busca um hospital pelo seu ID interno]
    # [ENTRADA: hospital_id - ID interno do hospital a ser buscado]
    # [SAIDA: Optional[Hospital] - hospital ou None se não existir]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_by_id(self, hospital_id: int) -> Optional[Hospital]:
        return self.db.query(Hospital).filter(Hospital.id == hospital_id).first()
    
    # [GET HOSPITAL BY PUBLIC ID]
    # [Busca um hospital pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do hospital a ser buscado]
    # [SAIDA: Optional[Hospital] - hospital ou None se não existir]
    # [DEPENDENCIAS: self.db, Hospital, UUID]
    def get_by_public_id(self, public_id: UUID) -> Optional[Hospital]:
        return self.db.query(Hospital).filter(Hospital.public_id == public_id).first()

    # [GET HOSPITAL BY NAME]
    # [Busca um hospital pelo seu nome]
    # [ENTRADA: name - nome do hospital a ser buscado]
    # [SAIDA: Optional[Hospital] - hospital encontrado ou None se não existir]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_by_name(self, name: str) -> Optional[Hospital]:
        return self.db.query(Hospital).filter(Hospital.name == name).first()

    # [GET HOSPITAL BY DOCUMENT]
    # [Busca um hospital pelo documento]
    # [ENTRADA: document - documento do hospital a ser buscado]
    # [SAIDA: Optional[Hospital] - hospital encontrado ou None se não existir]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_by_document(self, document: str) -> Optional[Hospital]:
        return self.db.query(Hospital).filter(Hospital.document == document).first()

    # [GET HOSPITAL BY EMAIL]
    # [Busca um hospital pelo email]
    # [ENTRADA: email - email do hospital a ser buscado]
    # [SAIDA: Optional[Hospital] - hospital encontrado ou None se não existir]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_by_email(self, email: str) -> Optional[Hospital]:
        return self.db.query(Hospital).filter(Hospital.email == email).first()

    # [GET HOSPITAL BY PHONE]
    # [Busca um hospital pelo telefone]
    # [ENTRADA: phone - telefone do hospital a ser buscado]
    # [SAIDA: Optional[Hospital] - hospital encontrado ou None se não existir]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_by_phone(self, phone: str) -> Optional[Hospital]:
        return self.db.query(Hospital).filter(Hospital.phone == phone).first()

    # [GET HOSPITALS BY CITY]
    # [Busca hospitais pela cidade]
    # [ENTRADA: city - cidade dos hospitais, skip - registros a pular, limit - limite]
    # [SAIDA: list[Hospital] - lista de hospitais da cidade]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_by_city(self, city: str, skip: int = 0, limit: int = 100) -> list[Hospital]:
        return self.db.query(Hospital).filter(Hospital.city == city).offset(skip).limit(limit).all()

    # [GET HOSPITALS BY NATIONALITY]
    # [Busca hospitais pela nacionalidade]
    # [ENTRADA: nationality - nacionalidade dos hospitais, skip - registros a pular, limit - limite]
    # [SAIDA: list[Hospital] - lista de hospitais da nacionalidade]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_by_nationality(self, nationality: str, skip: int = 0, limit: int = 100) -> list[Hospital]:
        return self.db.query(Hospital).filter(Hospital.nationality == nationality).offset(skip).limit(limit).all()

    # [GET ALL HOSPITALS]
    # [Busca todos os hospitais com paginação]
    # [ENTRADA: skip - número de registros a pular, limit - limite de registros]
    # [SAIDA: list[Hospital] - lista de hospitais]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Hospital]:
        return self.db.query(Hospital).offset(skip).limit(limit).all()
    
    # [GET TOTAL COUNT]
    # [Conta o total de hospitais no banco de dados]
    # [ENTRADA: nenhuma]
    # [SAIDA: int - número total de hospitais]
    # [DEPENDENCIAS: self.db, Hospital]
    def get_total_count(self) -> int:
        return self.db.query(Hospital).count()

    # [UPDATE HOSPITAL]
    # [Atualiza um hospital existente no banco de dados]
    # [ENTRADA: hospital - instância do hospital, hospital_data - dados de atualização]
    # [SAIDA: Hospital - hospital atualizado com dados atuais do banco]
    # [DEPENDENCIAS: self.db]
    def update(self, hospital: Hospital, hospital_data: HospitalUpdate) -> Hospital:
        update_data = hospital_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(hospital, field, value)
        
        self.db.commit()
        self.db.refresh(hospital)
        return hospital

    # [DELETE HOSPITAL]
    # [Remove um hospital do banco de dados]
    # [ENTRADA: hospital - instância do hospital a ser removido]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, hospital: Hospital) -> None:
        self.db.delete(hospital)
        self.db.commit()
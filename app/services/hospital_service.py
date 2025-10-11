from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.hospital_repository import HospitalRepository
from app.schemas.hospital import HospitalCreate, HospitalUpdate
from app.models.hospital import Hospital
from app.validators.hospital_validator import HospitalValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [HOSPITAL SERVICE]
# [Serviço para gestão de hospitais com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância HospitalService configurada]
# [DEPENDENCIAS: HospitalRepository, HospitalValidator]
class HospitalService:
    
    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de hospital]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: HospitalRepository, HospitalValidator]
    def __init__(self, db: Session):
        self.hospital_repository = HospitalRepository(db)
        self.hospital_validator = HospitalValidator()

    # [CREATE HOSPITAL]
    # [Cria novo hospital com validação e verificação de duplicatas]
    # [ENTRADA: hospital_data - dados do hospital via HospitalCreate]
    # [SAIDA: Hospital - hospital criado ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.hospital_validator, self.hospital_repository]
    def create_hospital(self, hospital_data: HospitalCreate) -> Hospital:
        validation_result = self.hospital_validator.validate(hospital_data)
        if not validation_result.is_valid:
            errors = validation_result.get_errors_by_field()
            error_messages = []
            for field, messages in errors.items():
                for msg in messages:
                    error_messages.append(f"{field}: {msg}")

            raise HTTPException(
                status_code=422,
                detail={
                    "error": True,
                    "message": f"Validation error: {'; '.join(error_messages)}",
                    "status_code": 422
                }
            )

        # Check for unique constraints
        if self.hospital_repository.get_by_name(hospital_data.name):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Hospital with name '{hospital_data.name}' already exists",
                    "status_code": 409
                }
            )

        if self.hospital_repository.get_by_document(hospital_data.document):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Hospital with document '{hospital_data.document}' already exists",
                    "status_code": 409
                }
            )

        if self.hospital_repository.get_by_email(hospital_data.email):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Hospital with email '{hospital_data.email}' already exists",
                    "status_code": 409
                }
            )

        if self.hospital_repository.get_by_phone(hospital_data.phone):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Hospital with phone '{hospital_data.phone}' already exists",
                    "status_code": 409
                }
            )

        hospital = self.hospital_repository.create(hospital_data)
        return hospital

    # [GET HOSPITAL BY PUBLIC ID]
    # [Busca um hospital pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do hospital]
    # [SAIDA: Optional[Hospital] - hospital encontrado ou None]
    # [DEPENDENCIAS: self.hospital_repository]
    def get_hospital_by_public_id(self, public_id: UUID) -> Optional[Hospital]:
        return self.hospital_repository.get_by_public_id(public_id)

    # [GET HOSPITAL BY NAME]
    # [Busca um hospital pelo seu nome]
    # [ENTRADA: name - nome do hospital]
    # [SAIDA: Optional[Hospital] - hospital encontrado ou None]
    # [DEPENDENCIAS: self.hospital_repository]
    def get_hospital_by_name(self, name: str) -> Optional[Hospital]:
        return self.hospital_repository.get_by_name(name)

    # [GET HOSPITAL BY DOCUMENT]
    # [Busca um hospital pelo seu documento]
    # [ENTRADA: document - documento do hospital]
    # [SAIDA: Optional[Hospital] - hospital encontrado ou None]
    # [DEPENDENCIAS: self.hospital_repository]
    def get_hospital_by_document(self, document: str) -> Optional[Hospital]:
        return self.hospital_repository.get_by_document(document)

    # [GET HOSPITALS BY CITY]
    # [Busca hospitais por cidade com paginação]
    # [ENTRADA: city - cidade, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[Hospital] - hospitais paginados da cidade]
    # [DEPENDENCIAS: self.hospital_repository, PaginatedResponse]
    def get_hospitals_by_city(self, city: str, pagination: PaginationParams) -> PaginatedResponse[Hospital]:
        hospitals = self.hospital_repository.get_by_city(
            city=city,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.hospital_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=hospitals,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET HOSPITALS BY NATIONALITY]
    # [Busca hospitais por nacionalidade com paginação]
    # [ENTRADA: nationality - nacionalidade, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[Hospital] - hospitais paginados da nacionalidade]
    # [DEPENDENCIAS: self.hospital_repository, PaginatedResponse]
    def get_hospitals_by_nationality(self, nationality: str, pagination: PaginationParams) -> PaginatedResponse[Hospital]:
        hospitals = self.hospital_repository.get_by_nationality(
            nationality=nationality,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.hospital_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=hospitals,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [GET PAGINATED HOSPITALS]
    # [Busca hospitais com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[Hospital] - hospitais paginados com metadados]
    # [DEPENDENCIAS: self.hospital_repository, PaginatedResponse]
    def get_paginated_hospitals(self, pagination: PaginationParams) -> PaginatedResponse[Hospital]:
        hospitals = self.hospital_repository.get_all(
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.hospital_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=hospitals,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE HOSPITAL]
    # [Atualiza um hospital existente]
    # [ENTRADA: public_id - UUID público do hospital, hospital_data - dados de atualização]
    # [SAIDA: Optional[Hospital] - hospital atualizado ou None se não encontrado]
    # [DEPENDENCIAS: self.hospital_repository]
    def update_hospital(self, public_id: UUID, hospital_data: HospitalUpdate) -> Optional[Hospital]:
        hospital = self.hospital_repository.get_by_public_id(public_id)
        if not hospital:
            return None
        
        # Check for conflicts if fields are being updated
        if hospital_data.name and hospital_data.name != hospital.name:
            existing_hospital = self.hospital_repository.get_by_name(hospital_data.name)
            if existing_hospital:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Hospital with name '{hospital_data.name}' already exists",
                        "status_code": 409
                    }
                )

        if hospital_data.document and hospital_data.document != hospital.document:
            existing_hospital = self.hospital_repository.get_by_document(hospital_data.document)
            if existing_hospital:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Hospital with document '{hospital_data.document}' already exists",
                        "status_code": 409
                    }
                )

        if hospital_data.email and hospital_data.email != hospital.email:
            existing_hospital = self.hospital_repository.get_by_email(hospital_data.email)
            if existing_hospital:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Hospital with email '{hospital_data.email}' already exists",
                        "status_code": 409
                    }
                )

        if hospital_data.phone and hospital_data.phone != hospital.phone:
            existing_hospital = self.hospital_repository.get_by_phone(hospital_data.phone)
            if existing_hospital:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Hospital with phone '{hospital_data.phone}' already exists",
                        "status_code": 409
                    }
                )
        
        return self.hospital_repository.update(hospital, hospital_data)

    # [DELETE HOSPITAL]
    # [Remove um hospital do sistema]
    # [ENTRADA: public_id - UUID público do hospital a ser removido]
    # [SAIDA: bool - True se removido, False se não encontrado]
    # [DEPENDENCIAS: self.hospital_repository]
    def delete_hospital(self, public_id: UUID) -> bool:
        hospital = self.hospital_repository.get_by_public_id(public_id)
        if not hospital:
            return False
        
        self.hospital_repository.delete(hospital)
        return True
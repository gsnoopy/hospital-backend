from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.public_acquisition_repository import PublicAcquisitionRepository
from app.schemas.public_acquisition import PublicAcquisitionCreate, PublicAcquisitionUpdate
from app.models.public_acquisition import PublicAcquisition
from app.validators.public_acquisition_validator import PublicAcquisitionValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from uuid import UUID


# [PUBLIC ACQUISITION SERVICE]
# [Serviço para gestão de licitações públicas com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância PublicAcquisitionService configurada]
# [DEPENDENCIAS: PublicAcquisitionRepository, PublicAcquisitionValidator]
class PublicAcquisitionService:

    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de licitação]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: PublicAcquisitionRepository, PublicAcquisitionValidator]
    def __init__(self, db: Session):
        self.public_acquisition_repository = PublicAcquisitionRepository(db)
        self.public_acquisition_validator = PublicAcquisitionValidator()

    # [CREATE PUBLIC ACQUISITION]
    # [Cria nova licitação com validação e verificação de duplicatas]
    # [ENTRADA: public_acquisition_data - dados da licitação via PublicAcquisitionCreate, hospital_id - ID interno do hospital]
    # [SAIDA: PublicAcquisition - licitação criada ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.public_acquisition_validator, self.public_acquisition_repository]
    def create_public_acquisition(self, public_acquisition_data: PublicAcquisitionCreate, hospital_id: int) -> PublicAcquisition:
        from app.repositories.user_repository import UserRepository

        validation_result = self.public_acquisition_validator.validate(public_acquisition_data)
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

        # Validate that user exists and is a Pregoeiro in the same hospital
        user_repo = UserRepository(self.public_acquisition_repository.db)
        user = user_repo.get_by_public_id(public_acquisition_data.user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"User with ID '{public_acquisition_data.user_id}' not found",
                    "status_code": 404
                }
            )

        if user.role.name != "Pregoeiro":
            raise HTTPException(
                status_code=422,
                detail={
                    "error": True,
                    "message": "Only users with role 'Pregoeiro' can be associated with public acquisitions",
                    "status_code": 422
                }
            )

        if user.hospital_id != hospital_id:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": True,
                    "message": "User must belong to the same hospital as the public acquisition",
                    "status_code": 422
                }
            )

        # Check if code is unique within the hospital
        if self.public_acquisition_repository.get_by_code(public_acquisition_data.code, hospital_id):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Public acquisition with code '{public_acquisition_data.code}' already exists",
                    "status_code": 409
                }
            )

        public_acquisition = self.public_acquisition_repository.create(public_acquisition_data, hospital_id, user.id)
        return public_acquisition

    # [GET PUBLIC ACQUISITION BY PUBLIC ID]
    # [Busca uma licitação pelo seu UUID público]
    # [ENTRADA: public_id - UUID público da licitação, hospital_id - ID interno do hospital]
    # [SAIDA: PublicAcquisition - licitação encontrada ou exceção se não encontrada]
    # [DEPENDENCIAS: self.public_acquisition_repository]
    def get_public_acquisition_by_public_id(self, public_id: UUID, hospital_id: int) -> PublicAcquisition:
        public_acquisition = self.public_acquisition_repository.get_by_public_id(public_id, hospital_id)
        if not public_acquisition:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Public acquisition with ID '{public_id}' not found",
                    "status_code": 404
                }
            )
        return public_acquisition

    # [GET PAGINATED PUBLIC ACQUISITIONS]
    # [Busca licitações com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[PublicAcquisition] - licitações paginadas com metadados]
    # [DEPENDENCIAS: self.public_acquisition_repository, PaginatedResponse]
    def get_paginated_public_acquisitions(self, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[PublicAcquisition]:
        public_acquisitions = self.public_acquisition_repository.get_all(
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.public_acquisition_repository.get_total_count(hospital_id)

        return PaginatedResponse.create(
            items=public_acquisitions,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [SEARCH PUBLIC ACQUISITIONS]
    # [Busca licitações por termo de pesquisa com paginação]
    # [ENTRADA: search_term - termo de busca, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[PublicAcquisition] - licitações encontradas paginadas]
    # [DEPENDENCIAS: self.public_acquisition_repository, PaginatedResponse]
    def search_public_acquisitions(self, search_term: str, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[PublicAcquisition]:
        public_acquisitions = self.public_acquisition_repository.search_by_title(
            search_term=search_term,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.public_acquisition_repository.get_search_count(search_term, hospital_id)

        return PaginatedResponse.create(
            items=public_acquisitions,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [SEARCH PUBLIC ACQUISITIONS BY CODE]
    # [Busca licitações por código com paginação]
    # [ENTRADA: search_term - termo de busca, pagination - parâmetros de paginação, hospital_id - ID interno do hospital]
    # [SAIDA: PaginatedResponse[PublicAcquisition] - licitações encontradas paginadas]
    # [DEPENDENCIAS: self.public_acquisition_repository, PaginatedResponse]
    def search_public_acquisitions_by_code(self, search_term: str, pagination: PaginationParams, hospital_id: int) -> PaginatedResponse[PublicAcquisition]:
        public_acquisitions = self.public_acquisition_repository.search_by_code(
            search_term=search_term,
            hospital_id=hospital_id,
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.public_acquisition_repository.get_code_search_count(search_term, hospital_id)

        return PaginatedResponse.create(
            items=public_acquisitions,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE PUBLIC ACQUISITION]
    # [Atualiza uma licitação existente]
    # [ENTRADA: public_id - UUID público da licitação, public_acquisition_data - dados de atualização, hospital_id - ID interno do hospital]
    # [SAIDA: PublicAcquisition - licitação atualizada ou exceção se não encontrada]
    # [DEPENDENCIAS: self.public_acquisition_repository]
    def update_public_acquisition(self, public_id: UUID, public_acquisition_data: PublicAcquisitionUpdate, hospital_id: int) -> PublicAcquisition:
        from app.repositories.user_repository import UserRepository

        public_acquisition = self.public_acquisition_repository.get_by_public_id(public_id, hospital_id)
        if not public_acquisition:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Public acquisition with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        # Validate user if being updated
        if public_acquisition_data.user_id:
            user_repo = UserRepository(self.public_acquisition_repository.db)
            user = user_repo.get_by_public_id(public_acquisition_data.user_id)

            if not user:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "error": True,
                        "message": f"User with ID '{public_acquisition_data.user_id}' not found",
                        "status_code": 404
                    }
                )

            if user.role.name != "Pregoeiro":
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": True,
                        "message": "Only users with role 'Pregoeiro' can be associated with public acquisitions",
                        "status_code": 422
                    }
                )

            if user.hospital_id != hospital_id:
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": True,
                        "message": "User must belong to the same hospital as the public acquisition",
                        "status_code": 422
                    }
                )

        # Check for conflicts if code is being updated
        if public_acquisition_data.code and public_acquisition_data.code != public_acquisition.code:
            existing_public_acquisition = self.public_acquisition_repository.get_by_code(public_acquisition_data.code, hospital_id)
            if existing_public_acquisition:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Public acquisition with code '{public_acquisition_data.code}' already exists",
                        "status_code": 409
                    }
                )

        return self.public_acquisition_repository.update(public_acquisition, public_acquisition_data)

    # [DELETE PUBLIC ACQUISITION]
    # [Remove uma licitação do sistema]
    # [ENTRADA: public_id - UUID público da licitação a ser removida, hospital_id - ID interno do hospital]
    # [SAIDA: None - exceção se não encontrada]
    # [DEPENDENCIAS: self.public_acquisition_repository]
    def delete_public_acquisition(self, public_id: UUID, hospital_id: int) -> None:
        public_acquisition = self.public_acquisition_repository.get_by_public_id(public_id, hospital_id)
        if not public_acquisition:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": True,
                    "message": f"Public acquisition with ID '{public_id}' not found",
                    "status_code": 404
                }
            )

        self.public_acquisition_repository.delete(public_acquisition)

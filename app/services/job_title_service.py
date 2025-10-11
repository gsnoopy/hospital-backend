from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.job_title_repository import JobTitleRepository
from app.schemas.job_title import JobTitleCreate, JobTitleUpdate
from app.models.job_title import JobTitle
from app.validators.job_title_validator import JobTitleValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [JOB TITLE SERVICE]
# [Serviço para gestão de cargos com validações e verificações de duplicatas]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância JobTitleService configurada]
# [DEPENDENCIAS: JobTitleRepository, JobTitleValidator]
class JobTitleService:
    
    # [INIT]
    # [Construtor que inicializa o serviço com repository e validator de cargo]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: JobTitleRepository, JobTitleValidator]
    def __init__(self, db: Session):
        self.job_title_repository = JobTitleRepository(db)
        self.job_title_validator = JobTitleValidator()

    # [CREATE JOB TITLE]
    # [Cria novo cargo com validação e verificação de duplicatas]
    # [ENTRADA: job_title_data - dados do cargo via JobTitleCreate]
    # [SAIDA: JobTitle - cargo criado ou exceções de validação/duplicata]
    # [DEPENDENCIAS: self.job_title_validator, self.job_title_repository]
    def create_job_title(self, job_title_data: JobTitleCreate) -> JobTitle:
        validation_result = self.job_title_validator.validate(job_title_data)
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

        # Check for unique title constraint (optional business rule)
        if self.job_title_repository.get_by_title(job_title_data.title):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"JobTitle with title '{job_title_data.title}' already exists",
                    "status_code": 409
                }
            )

        job_title = self.job_title_repository.create(job_title_data)
        return job_title

    # [GET JOB TITLE BY PUBLIC ID]
    # [Busca um cargo pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do cargo]
    # [SAIDA: Optional[JobTitle] - cargo encontrado ou None]
    # [DEPENDENCIAS: self.job_title_repository]
    def get_job_title_by_public_id(self, public_id: UUID) -> Optional[JobTitle]:
        return self.job_title_repository.get_by_public_id(public_id)

    # [GET JOB TITLE BY TITLE]
    # [Busca um cargo pelo seu título]
    # [ENTRADA: title - título do cargo]
    # [SAIDA: Optional[JobTitle] - cargo encontrado ou None]
    # [DEPENDENCIAS: self.job_title_repository]
    def get_job_title_by_title(self, title: str) -> Optional[JobTitle]:
        return self.job_title_repository.get_by_title(title)

    # [GET PAGINATED JOB TITLES]
    # [Busca cargos com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[JobTitle] - cargos paginados com metadados]
    # [DEPENDENCIAS: self.job_title_repository, PaginatedResponse]
    def get_paginated_job_titles(self, pagination: PaginationParams) -> PaginatedResponse[JobTitle]:
        job_titles = self.job_title_repository.get_all(
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.job_title_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=job_titles,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE JOB TITLE]
    # [Atualiza um cargo existente]
    # [ENTRADA: public_id - UUID público do cargo, job_title_data - dados de atualização]
    # [SAIDA: Optional[JobTitle] - cargo atualizado ou None se não encontrado]
    # [DEPENDENCIAS: self.job_title_repository]
    def update_job_title(self, public_id: UUID, job_title_data: JobTitleUpdate) -> Optional[JobTitle]:
        job_title = self.job_title_repository.get_by_public_id(public_id)
        if not job_title:
            return None
        
        # Check for title conflicts if title is being updated
        if job_title_data.title and job_title_data.title != job_title.title:
            existing_job_title = self.job_title_repository.get_by_title(job_title_data.title)
            if existing_job_title:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"JobTitle with title '{job_title_data.title}' already exists",
                        "status_code": 409
                    }
                )
        
        return self.job_title_repository.update(job_title, job_title_data)

    # [DELETE JOB TITLE]
    # [Remove um cargo do sistema]
    # [ENTRADA: public_id - UUID público do cargo a ser removido]
    # [SAIDA: bool - True se removido, False se não encontrado]
    # [DEPENDENCIAS: self.job_title_repository]
    def delete_job_title(self, public_id: UUID) -> bool:
        job_title = self.job_title_repository.get_by_public_id(public_id)
        if not job_title:
            return False
        
        self.job_title_repository.delete(job_title)
        return True
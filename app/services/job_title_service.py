from sqlalchemy.orm import Session
from app.repositories.job_title_repository import JobTitleRepository
from app.schemas.job_title import JobTitleCreate, JobTitleUpdate
from app.models.job_title import JobTitle
from app.validators.job_title_validator import JobTitleValidator
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.core.exceptions import (
    ValidationException,
    DuplicateResourceException
)
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
            raise ValidationException(errors)
        
        # Check for unique title constraint (optional business rule)
        if self.job_title_repository.get_by_title(job_title_data.title):
            raise DuplicateResourceException("JobTitle", "title", job_title_data.title)

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

    # [GET JOB TITLES BY DEPARTMENT]
    # [Busca cargos por departamento com paginação]
    # [ENTRADA: department - departamento, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[JobTitle] - cargos paginados do departamento]
    # [DEPENDENCIAS: self.job_title_repository, PaginatedResponse]
    def get_job_titles_by_department(self, department: str, pagination: PaginationParams) -> PaginatedResponse[JobTitle]:
        job_titles = self.job_title_repository.get_by_department(
            department=department,
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

    # [GET JOB TITLES BY SENIORITY LEVEL]
    # [Busca cargos por nível de senioridade com paginação]
    # [ENTRADA: seniority_level - nível de senioridade, pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[JobTitle] - cargos paginados do nível]
    # [DEPENDENCIAS: self.job_title_repository, PaginatedResponse]
    def get_job_titles_by_seniority_level(self, seniority_level: str, pagination: PaginationParams) -> PaginatedResponse[JobTitle]:
        job_titles = self.job_title_repository.get_by_seniority_level(
            seniority_level=seniority_level,
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
                raise DuplicateResourceException("JobTitle", "title", job_title_data.title)
        
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
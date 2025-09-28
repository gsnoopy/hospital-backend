from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.job_title_service import JobTitleService
from app.schemas.job_title import JobTitleCreate, JobTitleUpdate, JobTitleResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_auth, require_roles
from app.models.user import User
from uuid import UUID

# [JOB TITLE ROUTER]
# [Router FastAPI para endpoints CRUD de cargos com prefixo /job-titles]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de cargos]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/job-titles", tags=["job-titles"])


# [CREATE JOB TITLE]
# [Endpoint POST para criar um novo cargo - requer autenticação]
# [ENTRADA: job_title_data - dados do cargo via JobTitleCreate, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: JobTitleResponse - cargo criado (status 201) ou HTTPException 422 com erros de validação]
# [DEPENDENCIAS: JobTitleService, ValidationException, HTTPException, status, require_auth]
@router.post("/", response_model=JobTitleResponse, status_code=status.HTTP_201_CREATED)
def create_job_title(
    job_title_data: JobTitleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    job_title_service = JobTitleService(db)
    return job_title_service.create_job_title(job_title_data)


# [GET JOB TITLES]
# [Endpoint GET para listar cargos com paginação - requer autenticação]
# [ENTRADA: page - número da página (min 1), size - itens por página (1-25), db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[JobTitleResponse] - lista paginada de cargos]
# [DEPENDENCIAS: PaginationParams, JobTitleService, require_auth]
@router.get("/", response_model=PaginatedResponse[JobTitleResponse])
def get_job_titles(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    job_title_service = JobTitleService(db)
    return job_title_service.get_paginated_job_titles(pagination)


# [GET JOB TITLE]
# [Endpoint GET para buscar um cargo pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público do cargo, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: JobTitleResponse - dados do cargo ou HTTPException 404 se não encontrado]
# [DEPENDENCIAS: JobTitleService, HTTPException, require_auth]
@router.get("/{public_id}", response_model=JobTitleResponse)
def get_job_title(
    public_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    job_title_service = JobTitleService(db)
    job_title = job_title_service.get_job_title_by_public_id(public_id)
    
    if not job_title:
        raise HTTPException(
            status_code=404,
            detail="Job title not found"
        )
    
    return job_title


# [GET JOB TITLE BY TITLE]
# [Endpoint GET para buscar um cargo pelo título - requer autenticação]
# [ENTRADA: title - título do cargo, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: JobTitleResponse - dados do cargo ou HTTPException 404 se não encontrado]
# [DEPENDENCIAS: JobTitleService, HTTPException, require_auth]
@router.get("/title/{title}", response_model=JobTitleResponse)
def get_job_title_by_title(
    title: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    job_title_service = JobTitleService(db)
    job_title = job_title_service.get_job_title_by_title(title)
    
    if not job_title:
        raise HTTPException(
            status_code=404,
            detail="Job title not found"
        )
    
    return job_title


# [GET JOB TITLES BY DEPARTMENT]
# [Endpoint GET para buscar cargos por departamento - requer autenticação]
# [ENTRADA: department - departamento dos cargos, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[JobTitleResponse] - lista paginada de cargos do departamento]
# [DEPENDENCIAS: JobTitleService, PaginationParams, require_auth]
@router.get("/department/{department}", response_model=PaginatedResponse[JobTitleResponse])
def get_job_titles_by_department(
    department: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    job_title_service = JobTitleService(db)
    return job_title_service.get_job_titles_by_department(department, pagination)


# [GET JOB TITLES BY SENIORITY LEVEL]
# [Endpoint GET para buscar cargos por nível de senioridade - requer autenticação]
# [ENTRADA: seniority_level - nível de senioridade, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[JobTitleResponse] - lista paginada de cargos do nível]
# [DEPENDENCIAS: JobTitleService, PaginationParams, require_auth]
@router.get("/seniority/{seniority_level}", response_model=PaginatedResponse[JobTitleResponse])
def get_job_titles_by_seniority_level(
    seniority_level: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    pagination = PaginationParams(page=page, size=size)
    job_title_service = JobTitleService(db)
    return job_title_service.get_job_titles_by_seniority_level(seniority_level, pagination)


# [UPDATE JOB TITLE]
# [Endpoint PUT para atualizar um cargo - requer autenticação]
# [ENTRADA: public_id - UUID público do cargo, job_title_data - dados de atualização, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: JobTitleResponse - cargo atualizado ou HTTPException 404]
# [DEPENDENCIAS: JobTitleService, HTTPException, require_auth]
@router.put("/{public_id}", response_model=JobTitleResponse)
def update_job_title(
    public_id: UUID,
    job_title_data: JobTitleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    job_title_service = JobTitleService(db)
    job_title = job_title_service.update_job_title(public_id, job_title_data)
    
    if not job_title:
        raise HTTPException(
            status_code=404,
            detail="Job title not found"
        )
    
    return job_title


# [DELETE JOB TITLE]
# [Endpoint DELETE para remover um cargo - requer autenticação]
# [ENTRADA: public_id - UUID público do cargo, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: dict - mensagem de sucesso ou HTTPException 404]
# [DEPENDENCIAS: JobTitleService, HTTPException, require_auth]
@router.delete("/{public_id}")
def delete_job_title(
    public_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    job_title_service = JobTitleService(db)
    success = job_title_service.delete_job_title(public_id)
    
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Job title not found"
        )
    
    return {"message": "Job title deleted successfully"}
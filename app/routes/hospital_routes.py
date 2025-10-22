from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.hospital_service import HospitalService
from app.schemas.hospital import HospitalCreate, HospitalUpdate, HospitalResponse
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.decorators import require_developer
from app.core.hospital_context import HospitalContext
from app.models.user import User
from uuid import UUID

# [HOSPITAL ROUTER]
# [Router FastAPI para endpoints CRUD de hospitais com prefixo /hospitals]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para gestão de hospitais]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/hospitals", tags=["hospitals"])


# [CREATE HOSPITAL]
# [Endpoint POST para criar um novo hospital - requer autenticação]
# [ENTRADA: hospital_data - dados do hospital via HospitalCreate, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: HospitalResponse - hospital criado (status 201) ou HTTPException 422 com erros de validação]
# [DEPENDENCIAS: HospitalService, ValidationException, HTTPException, status, require_auth]
@router.post("/", response_model=HospitalResponse, status_code=status.HTTP_201_CREATED)
def create_hospital(
    hospital_data: HospitalCreate,
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    hospital_service = HospitalService(db)
    return hospital_service.create_hospital(hospital_data)


# [GET HOSPITALS]
# [Endpoint GET para listar hospitais com paginação - requer autenticação]
# [ENTRADA: page - número da página (min 1), size - itens por página (1-25), db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[HospitalResponse] - lista paginada de hospitais]
# [DEPENDENCIAS: PaginationParams, HospitalService, require_auth]
@router.get("/", response_model=PaginatedResponse[HospitalResponse])
def get_hospitals(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    pagination = PaginationParams(page=page, size=size)
    hospital_service = HospitalService(db)
    return hospital_service.get_paginated_hospitals(pagination)


# [GET HOSPITAL]
# [Endpoint GET para buscar um hospital pelo UUID público - requer autenticação]
# [ENTRADA: public_id - UUID público do hospital, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: HospitalResponse - dados do hospital ou HTTPException 404 se não encontrado]
# [DEPENDENCIAS: HospitalService, HTTPException, require_auth]
@router.get("/{public_id}", response_model=HospitalResponse)
def get_hospital(
    public_id: UUID, 
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    hospital_service = HospitalService(db)
    hospital = hospital_service.get_hospital_by_public_id(public_id)
    
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    
    return hospital


# [GET HOSPITAL BY NAME]
# [Endpoint GET para buscar um hospital pelo nome - requer autenticação]
# [ENTRADA: name - nome do hospital, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: HospitalResponse - dados do hospital ou HTTPException 404 se não encontrado]
# [DEPENDENCIAS: HospitalService, HTTPException, require_auth]
@router.get("/name/{name}", response_model=HospitalResponse)
def get_hospital_by_name(
    name: str, 
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    hospital_service = HospitalService(db)
    hospital = hospital_service.get_hospital_by_name(name)
    
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    
    return hospital

# [GET HOSPITALS BY CITY]
# [Endpoint GET para buscar hospitais por cidade - requer autenticação]
# [ENTRADA: city - cidade dos hospitais, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[HospitalResponse] - lista paginada de hospitais da cidade]
# [DEPENDENCIAS: HospitalService, PaginationParams, require_auth]
@router.get("/city/{city}", response_model=PaginatedResponse[HospitalResponse])
def get_hospitals_by_city(
    city: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    pagination = PaginationParams(page=page, size=size)
    hospital_service = HospitalService(db)
    return hospital_service.get_hospitals_by_city(city, pagination)


# [GET HOSPITALS BY NATIONALITY]
# [Endpoint GET para buscar hospitais por nacionalidade - requer autenticação]
# [ENTRADA: nationality - nacionalidade dos hospitais, page - número da página, size - itens por página, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: PaginatedResponse[HospitalResponse] - lista paginada de hospitais da nacionalidade]
# [DEPENDENCIAS: HospitalService, PaginationParams, require_auth]
@router.get("/nationality/{nationality}", response_model=PaginatedResponse[HospitalResponse])
def get_hospitals_by_nationality(
    nationality: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    pagination = PaginationParams(page=page, size=size)
    hospital_service = HospitalService(db)
    return hospital_service.get_hospitals_by_nationality(nationality, pagination)


# [UPDATE HOSPITAL]
# [Endpoint PUT para atualizar um hospital - requer autenticação]
# [ENTRADA: public_id - UUID público do hospital, hospital_data - dados de atualização, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: HospitalResponse - hospital atualizado ou HTTPException 404]
# [DEPENDENCIAS: HospitalService, HTTPException, require_auth]
@router.put("/{public_id}", response_model=HospitalResponse)
def update_hospital(
    public_id: UUID,
    hospital_data: HospitalUpdate,
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    hospital_service = HospitalService(db)
    hospital = hospital_service.update_hospital(public_id, hospital_data)
    
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    
    return hospital


# [DELETE HOSPITAL]
# [Endpoint DELETE para remover um hospital - requer autenticação]
# [ENTRADA: public_id - UUID público do hospital, db - sessão do banco, current_user - usuário autenticado]
# [SAIDA: dict - mensagem de sucesso ou HTTPException 404]
# [DEPENDENCIAS: HospitalService, HTTPException, require_auth]
@router.delete("/{public_id}")
def delete_hospital(
    public_id: UUID,
    db: Session = Depends(get_db),
    context: HospitalContext = Depends(require_developer())
):
    hospital_service = HospitalService(db)
    success = hospital_service.delete_hospital(public_id)
    
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )
    
    return {"message": "Hospital deleted successfully"}
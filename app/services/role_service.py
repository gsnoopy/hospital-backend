from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate
from app.models.role import Role
from app.schemas.pagination import PaginatedResponse, PaginationParams
from typing import Optional
from uuid import UUID


# [ROLE SERVICE]
# [Serviço para gestão de roles com regras de negócio e validações]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância RoleService configurada]
# [DEPENDENCIAS: RoleRepository]
class RoleService:
    
    # [INIT]
    # [Construtor que inicializa o serviço com repository de role]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: RoleRepository]
    def __init__(self, db: Session):
        self.role_repository = RoleRepository(db)

    # [CREATE ROLE]
    # [Cria uma nova role validando se o nome já existe]
    # [ENTRADA: role_data - dados da role via RoleCreate]
    # [SAIDA: Role - role criada ou UserAlreadyExistsException se nome já existe]
    # [DEPENDENCIAS: self.role_repository, UserAlreadyExistsException]
    def create_role(self, role_data: RoleCreate) -> Role:
        if self.role_repository.get_by_name(role_data.name):
            raise HTTPException(
                status_code=409,
                detail={
                    "error": True,
                    "message": f"Role with name '{role_data.name}' already exists",
                    "status_code": 409
                }
            )

        role = self.role_repository.create(role_data)
        return role

    # [GET ROLE BY PUBLIC ID]
    # [Busca uma role pelo seu UUID público]
    # [ENTRADA: public_id - UUID público da role]
    # [SAIDA: Optional[Role] - role encontrada ou None]
    # [DEPENDENCIAS: self.role_repository]
    def get_role_by_public_id(self, public_id: UUID) -> Optional[Role]:
        return self.role_repository.get_by_public_id(public_id)

    # [GET ROLE BY NAME]
    # [Busca uma role pelo seu nome]
    # [ENTRADA: name - nome da role]
    # [SAIDA: Optional[Role] - role encontrada ou None]
    # [DEPENDENCIAS: self.role_repository]
    def get_role_by_name(self, name: str) -> Optional[Role]:
        return self.role_repository.get_by_name(name)

    # [GET PAGINATED ROLES]
    # [Busca roles com paginação criando resposta com metadados]
    # [ENTRADA: pagination - parâmetros de paginação]
    # [SAIDA: PaginatedResponse[Role] - roles paginadas com metadados]
    # [DEPENDENCIAS: self.role_repository, PaginatedResponse]
    def get_paginated_roles(self, pagination: PaginationParams) -> PaginatedResponse[Role]:
        roles = self.role_repository.get_all(
            skip=pagination.get_offset(),
            limit=pagination.get_limit()
        )
        total = self.role_repository.get_total_count()
        
        return PaginatedResponse.create(
            items=roles,
            page=pagination.page,
            size=pagination.size,
            total=total
        )

    # [UPDATE ROLE]
    # [Atualiza uma role existente validando se novo nome já existe em outra role]
    # [ENTRADA: public_id - UUID público da role, role_data - novos dados]
    # [SAIDA: Optional[Role] - role atualizada ou None se não encontrada]
    # [DEPENDENCIAS: self.role_repository, HTTPException]
    def update_role(self, public_id: UUID, role_data: RoleUpdate) -> Optional[Role]:
        role = self.role_repository.get_by_public_id(public_id)
        if not role:
            return None
            
        # Check for name conflicts if name is being updated
        if role_data.name and role_data.name != role.name:
            existing_role = self.role_repository.get_by_name(role_data.name)
            if existing_role:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": True,
                        "message": f"Role with name '{role_data.name}' already exists",
                        "status_code": 409
                    }
                )
        
        # Update fields
        update_data = role_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(role, field, value)
            
        return self.role_repository.update(role)

    # [DELETE ROLE]
    # [Remove uma role do sistema]
    # [ENTRADA: role - role a ser removida]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.role_repository]
    def delete_role(self, role: Role) -> None:
        self.role_repository.delete(role)
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate
from typing import Optional
from uuid import UUID


# [ROLE REPOSITORY]
# [Repository para operações CRUD da entidade Role no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância RoleRepository configurada]
# [DEPENDENCIAS: Session]
class RoleRepository:
    
    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE ROLE]
    # [Cria uma nova role no banco de dados a partir dos dados fornecidos]
    # [ENTRADA: role_data - dados da role via schema RoleCreate]
    # [SAIDA: Role - instância da role criada com ID gerado]
    # [DEPENDENCIAS: Role, self.db]
    def create(self, role_data: RoleCreate) -> Role:
        db_role = Role(
            name=role_data.name,
            description=role_data.description,
        )
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    # [GET ROLE BY ID]
    # [Busca uma role pelo seu ID interno]
    # [ENTRADA: role_id - ID interno da role a ser buscada]
    # [SAIDA: Optional[Role] - role encontrada ou None se não existir]
    # [DEPENDENCIAS: self.db, Role]
    def get_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    # [GET ROLE BY PUBLIC ID]
    # [Busca uma role pelo seu UUID público]
    # [ENTRADA: public_id - UUID público da role a ser buscada]
    # [SAIDA: Optional[Role] - role encontrada ou None se não existir]
    # [DEPENDENCIAS: self.db, Role, UUID]
    def get_by_public_id(self, public_id: UUID) -> Optional[Role]:
        return self.db.query(Role).filter(Role.public_id == public_id).first()

    # [GET ROLE BY NAME]
    # [Busca uma role pelo seu nome único]
    # [ENTRADA: name - nome da role a ser buscada]
    # [SAIDA: Optional[Role] - role encontrada ou None se não existir]
    # [DEPENDENCIAS: self.db, Role]
    def get_by_name(self, name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.name == name).first()

    # [GET ALL ROLES]
    # [Busca todas as roles com paginação]
    # [ENTRADA: skip - número de registros a pular, limit - limite de registros]
    # [SAIDA: list[Role] - lista de roles encontradas]
    # [DEPENDENCIAS: self.db, Role]
    def get_all(self, skip: int = 0, limit: int = 100) -> list[Role]:
        return self.db.query(Role).offset(skip).limit(limit).all()
    
    # [GET TOTAL COUNT]
    # [Conta o total de roles no banco de dados]
    # [ENTRADA: nenhuma]
    # [SAIDA: int - número total de roles]
    # [DEPENDENCIAS: self.db, Role]
    def get_total_count(self) -> int:
        return self.db.query(Role).count()

    # [UPDATE ROLE]
    # [Atualiza uma role existente no banco de dados]
    # [ENTRADA: role - instância da role já modificada]
    # [SAIDA: Role - role atualizada com dados atuais do banco]
    # [DEPENDENCIAS: self.db]
    def update(self, role: Role) -> Role:
        self.db.commit()
        self.db.refresh(role)
        return role

    # [DELETE ROLE]
    # [Remove uma role do banco de dados]
    # [ENTRADA: role - instância da role a ser removida]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, role: Role) -> None:
        self.db.delete(role)
        self.db.commit()
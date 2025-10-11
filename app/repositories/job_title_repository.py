from sqlalchemy.orm import Session
from app.models.job_title import JobTitle
from app.schemas.job_title import JobTitleCreate, JobTitleUpdate
from typing import Optional
from uuid import UUID

# [JOB TITLE REPOSITORY]
# [Repository para operações CRUD da entidade JobTitle no banco de dados]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância JobTitleRepository configurada]
# [DEPENDENCIAS: Session]
class JobTitleRepository:
    
    # [INIT]
    # [Construtor que inicializa o repository com uma sessão do banco]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: nenhuma]
    def __init__(self, db: Session):
        self.db = db

    # [CREATE JOB TITLE]
    # [Cria um novo cargo no banco de dados]
    # [ENTRADA: job_title_data - dados do cargo via schema]
    # [SAIDA: JobTitle - instância do cargo criado]
    # [DEPENDENCIAS: JobTitle, self.db]
    def create(self, job_title_data: JobTitleCreate) -> JobTitle:
        db_job_title = JobTitle(
            title=job_title_data.title,
        )
        self.db.add(db_job_title)
        self.db.commit()
        self.db.refresh(db_job_title)
        return db_job_title

    # [GET JOB TITLE BY ID]
    # [Busca um cargo pelo seu ID interno]
    # [ENTRADA: job_title_id - ID interno do cargo a ser buscado]
    # [SAIDA: Optional[JobTitle] - cargo ou None se não existir]
    # [DEPENDENCIAS: self.db, JobTitle]
    def get_by_id(self, job_title_id: int) -> Optional[JobTitle]:
        return self.db.query(JobTitle).filter(JobTitle.id == job_title_id).first()
    
    # [GET JOB TITLE BY PUBLIC ID]
    # [Busca um cargo pelo seu UUID público]
    # [ENTRADA: public_id - UUID público do cargo a ser buscado]
    # [SAIDA: Optional[JobTitle] - cargo ou None se não existir]
    # [DEPENDENCIAS: self.db, JobTitle, UUID]
    def get_by_public_id(self, public_id: UUID) -> Optional[JobTitle]:
        return self.db.query(JobTitle).filter(JobTitle.public_id == public_id).first()

    # [GET JOB TITLE BY TITLE]
    # [Busca um cargo pelo seu título]
    # [ENTRADA: title - título do cargo a ser buscado]
    # [SAIDA: Optional[JobTitle] - cargo encontrado ou None se não existir]
    # [DEPENDENCIAS: self.db, JobTitle]
    def get_by_title(self, title: str) -> Optional[JobTitle]:
        return self.db.query(JobTitle).filter(JobTitle.title == title).first()

    # [GET ALL JOB TITLES]
    # [Busca todos os cargos com paginação]
    # [ENTRADA: skip - número de registros a pular, limit - limite de registros]
    # [SAIDA: list[JobTitle] - lista de cargos]
    # [DEPENDENCIAS: self.db, JobTitle]
    def get_all(self, skip: int = 0, limit: int = 100) -> list[JobTitle]:
        return self.db.query(JobTitle).offset(skip).limit(limit).all()
    
    # [GET TOTAL COUNT]
    # [Conta o total de cargos no banco de dados]
    # [ENTRADA: nenhuma]
    # [SAIDA: int - número total de cargos]
    # [DEPENDENCIAS: self.db, JobTitle]
    def get_total_count(self) -> int:
        return self.db.query(JobTitle).count()

    # [UPDATE JOB TITLE]
    # [Atualiza um cargo existente no banco de dados]
    # [ENTRADA: job_title - instância do cargo, job_title_data - dados de atualização]
    # [SAIDA: JobTitle - cargo atualizado com dados atuais do banco]
    # [DEPENDENCIAS: self.db]
    def update(self, job_title: JobTitle, job_title_data: JobTitleUpdate) -> JobTitle:
        update_data = job_title_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job_title, field, value)
        
        self.db.commit()
        self.db.refresh(job_title)
        return job_title

    # [DELETE JOB TITLE]
    # [Remove um cargo do banco de dados]
    # [ENTRADA: job_title - instância do cargo a ser removido]
    # [SAIDA: None]
    # [DEPENDENCIAS: self.db]
    def delete(self, job_title: JobTitle) -> None:
        self.db.delete(job_title)
        self.db.commit()
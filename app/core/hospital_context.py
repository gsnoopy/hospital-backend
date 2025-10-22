from typing import Optional
from app.models.user import User
from sqlalchemy.orm import Query


# [HOSPITAL CONTEXT]
# [Classe que encapsula o contexto de autorização por hospital]
# [ENTRADA: user - usuário autenticado]
# [SAIDA: métodos para aplicar filtros de hospital automaticamente]
# [DEPENDENCIAS: User, Query]
class HospitalContext:
    """
    Contexto de autorização que gerencia filtros de hospital.

    - Desenvolvedor: sem restrições (vê todos os hospitais)
    - Outros roles: restritos ao próprio hospital
    """

    # [INIT]
    # [Inicializa o contexto com o usuário autenticado]
    # [ENTRADA: user - usuário autenticado]
    # [SAIDA: instância de HospitalContext]
    def __init__(self, user: User):
        self.user = user
        self.role = user.role.name if user.role else None
        self._hospital_id = user.hospital_id

    # [IS DEVELOPER]
    # [Verifica se o usuário é Desenvolvedor]
    # [ENTRADA: nenhuma]
    # [SAIDA: bool - True se for Desenvolvedor]
    @property
    def is_developer(self) -> bool:
        return self.role == "Desenvolvedor"

    # [HOSPITAL ID]
    # [Retorna o hospital_id para usar em filtros de query]
    # [ENTRADA: nenhuma]
    # [SAIDA: Optional[int] - ID do hospital ou None se Desenvolvedor]
    @property
    def hospital_id(self) -> Optional[int]:
        """
        Retorna None para Desenvolvedor (lista todos os hospitais nos filtros).
        Retorna hospital_id para outros roles (filtra pelo hospital).

        ⚠️ IMPORTANTE: Use apenas para FILTROS (GET/LIST).
        Para CREATE, o Desenvolvedor pode ter hospital e deve ser respeitado.
        """
        return None if self.is_developer else self._hospital_id

    # [RAW HOSPITAL ID]
    # [Retorna o hospital_id real do usuário (sem lógica de desenvolvedor)]
    # [ENTRADA: nenhuma]
    # [SAIDA: Optional[int] - ID do hospital do usuário ou None]
    @property
    def raw_hospital_id(self) -> Optional[int]:
        """
        Retorna o hospital_id REAL do usuário, independente do role.

        Use quando precisar do hospital_id do usuário autenticado,
        sem aplicar a lógica "Desenvolvedor vê tudo".
        """
        return self._hospital_id

    # [APPLY FILTER]
    # [Aplica filtro de hospital em uma query SQLAlchemy]
    # [ENTRADA: query - query SQLAlchemy, model - modelo com campo hospital_id]
    # [SAIDA: Query - query com filtro aplicado (se necessário)]
    def apply_filter(self, query: Query, model) -> Query:
        """
        Aplica filtro de hospital automaticamente.

        Args:
            query: Query SQLAlchemy
            model: Modelo SQLAlchemy com campo hospital_id

        Returns:
            Query filtrada (se não for Desenvolvedor)
        """
        if not self.is_developer and self._hospital_id:
            return query.filter(model.hospital_id == self._hospital_id)
        return query

    # [CAN ACCESS HOSPITAL]
    # [Verifica se o usuário pode acessar um hospital específico]
    # [ENTRADA: hospital_id - ID do hospital a verificar]
    # [SAIDA: bool - True se pode acessar]
    def can_access_hospital(self, hospital_id: int) -> bool:
        """
        Verifica se o usuário pode acessar um hospital.

        - Desenvolvedor: pode acessar qualquer hospital
        - Outros: apenas o próprio hospital
        """
        if self.is_developer:
            return True
        return self._hospital_id == hospital_id

    # [VALIDATE HOSPITAL ACCESS]
    # [Valida acesso ao hospital ou levanta exceção]
    # [ENTRADA: hospital_id - ID do hospital a validar]
    # [SAIDA: None ou HTTPException]
    def validate_hospital_access(self, hospital_id: int) -> None:
        """
        Valida se o usuário pode acessar o hospital.
        Levanta HTTPException 403 se não puder.
        """
        if not self.can_access_hospital(hospital_id):
            from fastapi import HTTPException
            raise HTTPException(
                status_code=403,
                detail="You can only access resources from your own hospital"
            )

    # [GET HOSPITAL ID FOR CREATE]
    # [Retorna o hospital_id a ser usado na criação de recursos]
    # [ENTRADA: requested_hospital_id - hospital_id passado no body (opcional)]
    # [SAIDA: int - hospital_id a usar]
    def get_hospital_id_for_create(self, requested_hospital_id: Optional[int] = None) -> Optional[int]:
        """
        Determina qual hospital_id usar na criação.

        - Desenvolvedor: usa o requested_hospital_id (se fornecido)
        - Outros: força usar o próprio hospital
        """
        if self.is_developer:
            return requested_hospital_id
        return self._hospital_id

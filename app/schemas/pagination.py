from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, TypeVar, Generic

T = TypeVar('T')

# [PAGINATION PARAMS]
# [Schema Pydantic para parâmetros de paginação com validação]
# [ENTRADA: page - número da página (min 1), size - itens por página (1-25)]
# [SAIDA: instância PaginationParams validada]
# [DEPENDENCIAS: BaseModel, Field]
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number (minimum 1)")
    size: int = Field(default=10, ge=1, le=25, description="Page size (1-25)")
    
    # [VALIDATE PAGE]
    # [Validador de campo para garantir que page seja maior que 0]
    # [ENTRADA: v - valor do campo page]
    # [SAIDA: int - valor validado ou ValueError se inválido]
    # [DEPENDENCIAS: field_validator]
    @field_validator('page')
    @classmethod
    def validate_page(cls, v):
        if v < 1:
            raise ValueError('Page must be greater than 0')
        return v
    
    # [VALIDATE SIZE]
    # [Validador de campo para garantir que size esteja entre 1 e 25]
    # [ENTRADA: v - valor do campo size]
    # [SAIDA: int - valor validado ou ValueError se inválido]
    # [DEPENDENCIAS: field_validator]
    @field_validator('size')
    @classmethod
    def validate_size(cls, v):
        if v < 1:
            raise ValueError('Size must be greater than 0')
        if v > 25:
            raise ValueError('Size cannot exceed 25 items per page')
        return v
    
    # [GET OFFSET]
    # [Calcula o offset para query SQL baseado na página e tamanho]
    # [ENTRADA: self - instância com page e size]
    # [SAIDA: int - offset calculado para SQL]
    # [DEPENDENCIAS: nenhuma]
    def get_offset(self) -> int:
        return (self.page - 1) * self.size
    
    # [GET LIMIT]
    # [Retorna o limite de registros para query SQL]
    # [ENTRADA: self - instância com size]
    # [SAIDA: int - limite para SQL]
    # [DEPENDENCIAS: nenhuma]
    def get_limit(self) -> int:
        return self.size

# [PAGINATED RESPONSE]
# [Schema Pydantic genérico para resposta paginada com metadados]
# [ENTRADA: items - lista de itens tipo T, page/size/total/pages - metadados de paginação, has_next/has_prev - flags de navegação]
# [SAIDA: instância PaginatedResponse[T] para resposta da API]
# [DEPENDENCIAS: BaseModel, Generic, List, ConfigDict]
class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    items: List[T]
    page: int
    size: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool
    
    # [CREATE]
    # [Método de classe para criar instância PaginatedResponse com cálculos automáticos]
    # [ENTRADA: items - lista de itens, page - página atual, size - itens por página, total - total de registros]
    # [SAIDA: PaginatedResponse[T] - instância com metadados calculados]
    # [DEPENDENCIAS: nenhuma]
    @classmethod
    def create(
        cls,
        items: List[T],
        page: int,
        size: int,
        total: int
    ) -> 'PaginatedResponse[T]':
        pages = (total + size - 1) // size
        return cls(
            items=items,
            page=page,
            size=size,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )
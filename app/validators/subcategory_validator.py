import re
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.subcategory import SubCategoryCreate


# [SUBCATEGORY VALIDATOR]
# [Validador customizado para dados de subcategoria com regras específicas do negócio]
# [ENTRADA: data - SubCategoryCreate com dados da subcategoria]
# [SAIDA: ValidationResult com resultado da validação]
# [DEPENDENCIAS: BaseValidator, ValidationResult, re]
class SubCategoryValidator(BaseValidator):

    # [VALIDATE]
    # [Método principal que executa todas as validações dos campos da subcategoria]
    # [ENTRADA: data - SubCategoryCreate com dados da subcategoria]
    # [SAIDA: ValidationResult - resultado consolidado de todas as validações]
    # [DEPENDENCIAS: ValidationResult, métodos privados de validação]
    def validate(self, data: SubCategoryCreate) -> ValidationResult:
        result = ValidationResult()

        self._validate_name(data.name, result)
        self._validate_description(data.description, result)
        self._validate_category_id(data.category_id, result)

        return result

    # [VALIDATE NAME]
    # [Valida nome da subcategoria - tamanho, caracteres permitidos]
    # [ENTRADA: name - nome a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_name(self, name: str, result: ValidationResult):
        if not name or len(name.strip()) < 2:
            result.add_error("SubCategory name must be at least 2 characters long", "name")

        if len(name) > 100:
            result.add_error("SubCategory name must be less than 100 characters", "name")

        # Nome deve conter apenas letras, números, espaços e alguns caracteres especiais
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-\&\(\)\.]+$", name):
            result.add_error("SubCategory name must contain only letters, numbers, spaces, hyphens, ampersands, and parentheses", "name")

    # [VALIDATE DESCRIPTION]
    # [Valida descrição da subcategoria - tamanho máximo]
    # [ENTRADA: description - descrição a ser validada, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_description(self, description: str, result: ValidationResult):
        if description and len(description) > 500:
            result.add_error("SubCategory description must be less than 500 characters", "description")

    # [VALIDATE CATEGORY ID]
    # [Valida se o category_id é um UUID válido]
    # [ENTRADA: category_id - UUID da categoria, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_category_id(self, category_id, result: ValidationResult):
        if not category_id:
            result.add_error("Category ID is required", "category_id")
        else:
            # Validação adicional do UUID será feita pelo Pydantic
            # Aqui podemos adicionar validações de negócio se necessário
            pass
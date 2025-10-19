import re
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.items import ItemCreate


# [ITEM VALIDATOR]
# [Validador customizado para dados de item com regras específicas do negócio]
# [ENTRADA: data - ItemCreate com dados do item]
# [SAIDA: ValidationResult com resultado da validação]
# [DEPENDENCIAS: BaseValidator, ValidationResult, re]
class ItemValidator(BaseValidator):

    # [VALIDATE]
    # [Método principal que executa todas as validações dos campos do item]
    # [ENTRADA: data - ItemCreate com dados do item]
    # [SAIDA: ValidationResult - resultado consolidado de todas as validações]
    # [DEPENDENCIAS: ValidationResult, métodos privados de validação]
    def validate(self, data: ItemCreate) -> ValidationResult:
        result = ValidationResult()

        self._validate_name(data.name, result)
        self._validate_similar_names(data.similar_names, result)
        self._validate_description(data.description, result)
        self._validate_full_description(data.full_description, result)
        self._validate_internal_code(data.internal_code, result)
        self._validate_presentation(data.presentation, result)
        self._validate_sample(data.sample, result)

        return result

    # [VALIDATE NAME]
    # [Valida nome do item - tamanho, caracteres permitidos]
    # [ENTRADA: name - nome a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_name(self, name: str, result: ValidationResult):
        if not name or len(name.strip()) < 2:
            result.add_error("Item name must be at least 2 characters long", "name")

        if len(name) > 200:
            result.add_error("Item name must be less than 200 characters", "name")

        # Nome deve conter apenas letras, números, espaços e alguns caracteres especiais
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-\&\(\)\.\,\/\+]+$", name):
            result.add_error("Item name contains invalid characters", "name")

    # [VALIDATE SIMILAR NAMES]
    # [Valida similar_names do item - lista de strings]
    # [ENTRADA: similar_names - lista de nomes similares a ser validada, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error, re]
    def _validate_similar_names(self, similar_names: list, result: ValidationResult):
        if similar_names is not None:
            if not isinstance(similar_names, list):
                result.add_error("Similar names must be a list", "similar_names")
                return

            if len(similar_names) > 20:
                result.add_error("Similar names list must have at most 20 items", "similar_names")

            for idx, name in enumerate(similar_names):
                if not isinstance(name, str):
                    result.add_error(f"Similar name at index {idx} must be a string", "similar_names")
                    continue

                if len(name.strip()) < 2:
                    result.add_error(f"Similar name at index {idx} must be at least 2 characters", "similar_names")

                if len(name) > 200:
                    result.add_error(f"Similar name at index {idx} must be less than 200 characters", "similar_names")

                if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-\&\(\)\.\,\/\+]+$", name):
                    result.add_error(f"Similar name at index {idx} contains invalid characters", "similar_names")

    # [VALIDATE DESCRIPTION]
    # [Valida descrição do item - tamanho máximo]
    # [ENTRADA: description - descrição a ser validada, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_description(self, description: str, result: ValidationResult):
        if description and len(description) > 500:
            result.add_error("Item description must be less than 500 characters", "description")

    # [VALIDATE FULL DESCRIPTION]
    # [Valida descrição completa do item - tamanho máximo]
    # [ENTRADA: full_description - descrição completa a ser validada, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_full_description(self, full_description: str, result: ValidationResult):
        if full_description and len(full_description) > 2000:
            result.add_error("Item full description must be less than 2000 characters", "full_description")

    # [VALIDATE INTERNAL CODE]
    # [Valida código interno do item - formato alfanumérico]
    # [ENTRADA: internal_code - código interno a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_internal_code(self, internal_code: str, result: ValidationResult):
        if internal_code:
            if len(internal_code) > 50:
                result.add_error("Internal code must be less than 50 characters", "internal_code")

            if not re.match(r"^[a-zA-Z0-9\-\_]+$", internal_code):
                result.add_error("Internal code must contain only letters, numbers, hyphens and underscores", "internal_code")

    # [VALIDATE PRESENTATION]
    # [Valida apresentação do item - tamanho máximo]
    # [ENTRADA: presentation - apresentação a ser validada, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_presentation(self, presentation: str, result: ValidationResult):
        if presentation and len(presentation) > 100:
            result.add_error("Item presentation must be less than 100 characters", "presentation")

    # [VALIDATE SAMPLE]
    # [Valida quantidade de amostra - deve ser positiva]
    # [ENTRADA: sample - quantidade de amostra a ser validada, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_sample(self, sample: int, result: ValidationResult):
        if sample is not None and sample < 0:
            result.add_error("Sample quantity must be a positive number", "sample")

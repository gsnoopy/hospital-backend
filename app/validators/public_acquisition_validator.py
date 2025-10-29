import re
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.public_acquisition import PublicAcquisitionCreate


# [PUBLIC ACQUISITION VALIDATOR]
# [Validador customizado para dados de licitação pública com regras específicas do negócio]
# [ENTRADA: data - PublicAcquisitionCreate com dados da licitação]
# [SAIDA: ValidationResult com resultado da validação]
# [DEPENDENCIAS: BaseValidator, ValidationResult, re]
class PublicAcquisitionValidator(BaseValidator):

    # [VALIDATE]
    # [Método principal que executa todas as validações dos campos da licitação]
    # [ENTRADA: data - PublicAcquisitionCreate com dados da licitação]
    # [SAIDA: ValidationResult - resultado consolidado de todas as validações]
    # [DEPENDENCIAS: ValidationResult, métodos privados de validação]
    def validate(self, data: PublicAcquisitionCreate) -> ValidationResult:
        result = ValidationResult()

        self._validate_code(data.code, result)
        self._validate_title(data.title, result)

        return result

    # [VALIDATE CODE]
    # [Valida código da licitação - tamanho, caracteres permitidos]
    # [ENTRADA: code - código a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_code(self, code: str, result: ValidationResult):
        if not code or len(code.strip()) < 2:
            result.add_error("Public acquisition code must be at least 2 characters long", "code")

        if len(code) > 100:
            result.add_error("Public acquisition code must be less than 100 characters", "code")

        # Código deve conter apenas letras, números, espaços, hífens, barras e underscores
        if not re.match(r"^[a-zA-Z0-9\s\-\/\_]+$", code):
            result.add_error("Public acquisition code contains invalid characters", "code")

    # [VALIDATE TITLE]
    # [Valida título da licitação - tamanho, caracteres permitidos]
    # [ENTRADA: title - título a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_title(self, title: str, result: ValidationResult):
        if not title or len(title.strip()) < 5:
            result.add_error("Public acquisition title must be at least 5 characters long", "title")

        if len(title) > 500:
            result.add_error("Public acquisition title must be less than 500 characters", "title")

        # Título deve conter caracteres alfanuméricos e pontuação comum
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-\&\(\)\.\,\/\:\;\+\#\@]+$", title):
            result.add_error("Public acquisition title contains invalid characters", "title")

import re
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.job_title import JobTitleCreate


# [JOB TITLE VALIDATOR]
# [Validador customizado para dados de cargo com regras específicas do negócio]
# [ENTRADA: data - JobTitleCreate com dados do cargo]
# [SAIDA: ValidationResult com resultado da validação]
# [DEPENDENCIAS: BaseValidator, ValidationResult, re]
class JobTitleValidator(BaseValidator):

    # [VALIDATE]
    # [Método principal que executa todas as validações dos campos do cargo]
    # [ENTRADA: data - JobTitleCreate com dados do cargo]
    # [SAIDA: ValidationResult - resultado consolidado de todas as validações]
    # [DEPENDENCIAS: ValidationResult, métodos privados de validação]
    def validate(self, data: JobTitleCreate) -> ValidationResult:
        result = ValidationResult()

        self._validate_title(data.title, result)

        return result

    # [VALIDATE TITLE]
    # [Valida título do cargo - tamanho, caracteres permitidos]
    # [ENTRADA: title - título a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_title(self, title: str, result: ValidationResult):
        if not title or len(title.strip()) < 2:
            result.add_error("Title must be at least 2 characters long", "title")

        if len(title) > 100:
            result.add_error("Title must be less than 100 characters", "title")

        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s&./()-]+$", title):
            result.add_error("Title must contain only letters, numbers, spaces and basic punctuation (&./()-)", "title")
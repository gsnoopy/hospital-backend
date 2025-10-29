import re
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.supplier import SupplierCreate


# [SUPPLIER VALIDATOR]
# [Validador customizado para dados de fornecedor com regras específicas do negócio]
# [ENTRADA: data - SupplierCreate com dados do fornecedor]
# [SAIDA: ValidationResult com resultado da validação]
# [DEPENDENCIAS: BaseValidator, ValidationResult, re]
class SupplierValidator(BaseValidator):

    # [VALIDATE]
    # [Método principal que executa todas as validações dos campos do fornecedor]
    # [ENTRADA: data - SupplierCreate com dados do fornecedor]
    # [SAIDA: ValidationResult - resultado consolidado de todas as validações]
    # [DEPENDENCIAS: ValidationResult, métodos privados de validação]
    def validate(self, data: SupplierCreate) -> ValidationResult:
        result = ValidationResult()

        self._validate_name(data.name, result)
        self._validate_document_type(data.document_type, result)
        self._validate_document(data.document, data.document_type, result)
        self._validate_email(data.email, result)
        self._validate_phone(data.phone, result)

        return result

    # [VALIDATE NAME]
    # [Valida nome do fornecedor - tamanho, caracteres permitidos]
    # [ENTRADA: name - nome a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_name(self, name: str, result: ValidationResult):
        if not name or len(name.strip()) < 2:
            result.add_error("Supplier name must be at least 2 characters long", "name")

        if len(name) > 200:
            result.add_error("Supplier name must be less than 200 characters", "name")

        # Nome deve conter apenas letras, números, espaços e alguns caracteres especiais
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s\-\&\(\)\.\,\/]+$", name):
            result.add_error("Supplier name contains invalid characters", "name")

    # [VALIDATE DOCUMENT TYPE]
    # [Valida tipo de documento - deve ser CPF, CNPJ (Brasil), DNI, CUIT, CUIL (Argentina), CI, RUC (Paraguai)]
    # [ENTRADA: document_type - tipo de documento a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_document_type(self, document_type: str, result: ValidationResult):
        valid_types = ["CPF", "CNPJ", "DNI", "CUIT", "CUIL", "CI", "RUC"]
        if document_type not in valid_types:
            result.add_error(f"Document type must be one of: {', '.join(valid_types)}", "document_type")

    # [VALIDATE DOCUMENT]
    # [Valida documento - formato de acordo com o tipo para Brasil, Argentina e Paraguai]
    # [ENTRADA: document - documento a ser validado, document_type - tipo do documento, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_document(self, document: str, document_type: str, result: ValidationResult):
        if not document:
            result.add_error("Document is required", "document")
            return

        # Remove caracteres não numéricos
        clean_document = re.sub(r'\D', '', document)

        # Brasil
        if document_type == "CPF":
            if len(clean_document) != 11:
                result.add_error("CPF must have 11 digits", "document")
        elif document_type == "CNPJ":
            if len(clean_document) != 14:
                result.add_error("CNPJ must have 14 digits", "document")

        # Argentina
        elif document_type == "DNI":
            if len(clean_document) < 7 or len(clean_document) > 8:
                result.add_error("DNI must have 7 or 8 digits", "document")
        elif document_type == "CUIT":
            if len(clean_document) != 11:
                result.add_error("CUIT must have 11 digits", "document")
        elif document_type == "CUIL":
            if len(clean_document) != 11:
                result.add_error("CUIL must have 11 digits", "document")

        # Paraguai
        elif document_type == "CI":
            if len(clean_document) < 6 or len(clean_document) > 8:
                result.add_error("CI must have 6 to 8 digits", "document")
        elif document_type == "RUC":
            if len(clean_document) < 6 or len(clean_document) > 9:
                result.add_error("RUC must have 6 to 9 digits", "document")

    # [VALIDATE EMAIL]
    # [Valida formato do email]
    # [ENTRADA: email - email a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_email(self, email: str, result: ValidationResult):
        if not email:
            result.add_error("Email is required", "email")
            return

        # Regex básico para validar email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            result.add_error("Invalid email format", "email")

        if len(email) > 255:
            result.add_error("Email must be less than 255 characters", "email")

    # [VALIDATE PHONE]
    # [Valida formato do telefone]
    # [ENTRADA: phone - telefone a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_phone(self, phone: str, result: ValidationResult):
        if not phone:
            result.add_error("Phone is required", "phone")
            return

        # Remove caracteres não numéricos
        clean_phone = re.sub(r'\D', '', phone)

        # Telefone deve ter entre 10 e 11 dígitos (celular ou fixo com DDD)
        if len(clean_phone) < 10 or len(clean_phone) > 11:
            result.add_error("Phone must have 10 or 11 digits", "phone")

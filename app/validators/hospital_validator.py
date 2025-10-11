import re
from typing import List
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.hospital import HospitalCreate


# [HOSPITAL VALIDATOR]
# [Validador customizado para dados de hospital com regras específicas do negócio]
# [ENTRADA: data - HospitalCreate com dados do hospital]
# [SAIDA: ValidationResult com resultado da validação]
# [DEPENDENCIAS: BaseValidator, ValidationResult, re]
class HospitalValidator(BaseValidator):

    # [VALIDATE]
    # [Método principal que executa todas as validações dos campos do hospital]
    # [ENTRADA: data - HospitalCreate com dados do hospital]
    # [SAIDA: ValidationResult - resultado consolidado de todas as validações]
    # [DEPENDENCIAS: ValidationResult, métodos privados de validação]
    def validate(self, data: HospitalCreate) -> ValidationResult:
        result = ValidationResult()
        
        self._validate_name(data.name, result)
        self._validate_nationality(data.nationality, result)
        self._validate_document_type(data.document_type, result)
        self._validate_document(data.document, data.document_type, result)
        self._validate_email(data.email, result)
        self._validate_phone(data.phone, result)
        self._validate_city(data.city, result)
        
        return result
    
    # [VALIDATE NAME]
    # [Valida nome do hospital - tamanho, caracteres permitidos]
    # [ENTRADA: name - nome a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_name(self, name: str, result: ValidationResult):
        if not name or len(name.strip()) < 2:
            result.add_error("Name must be at least 2 characters long", "name")
        
        if len(name) > 200:
            result.add_error("Name must be less than 200 characters", "name")
        
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s&./()-]+$", name):
            result.add_error("Name must contain only letters, numbers, spaces and basic punctuation (&./()-)", "name")
    
    # [VALIDATE NATIONALITY]
    # [Valida nacionalidade - deve ser um dos valores permitidos]
    # [ENTRADA: nationality - nacionalidade a ser validada, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_nationality(self, nationality: str, result: ValidationResult):
        # Países do Mercosul e associados
        valid_nationalities = [
            "Brasileira", "Argentina", "Paraguaia", "Uruguaia", "Boliviana", "Chilena"
        ]

        if nationality not in valid_nationalities:
            result.add_error(f"Nationality must be one of: {', '.join(valid_nationalities)}", "nationality")

    # [VALIDATE DOCUMENT TYPE]
    # [Valida tipo do documento - deve ser um dos valores permitidos]
    # [ENTRADA: document_type - tipo do documento, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se tipo inválido]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_document_type(self, document_type: str, result: ValidationResult):
        # Tipos de documentos para empresas do Mercosul
        # CNPJ (Brasil), CUIT (Argentina), RUC (Paraguai), RUT (Chile/Uruguai), NIT (Bolívia)
        valid_types = ["CNPJ", "CUIT", "RUC", "RUT", "NIT", "OTHER"]

        if document_type not in valid_types:
            result.add_error(f"Document type must be one of: {', '.join(valid_types)}", "document_type")

    # [VALIDATE DOCUMENT]
    # [Valida documento baseado no tipo]
    # [ENTRADA: document - documento, document_type - tipo do documento, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se documento inválido]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_document(self, document: str, document_type: str, result: ValidationResult):
        if not document or len(document.strip()) < 5:
            result.add_error("Document must be at least 5 characters long", "document")
            return
        
        if len(document) > 30:
            result.add_error("Document must be less than 30 characters", "document")
            return

        if document_type == "CNPJ":
            self._validate_cnpj(document, result)
        elif document_type == "CUIT":
            self._validate_cuit(document, result)
        elif document_type == "RUC":
            self._validate_ruc(document, result)
        elif document_type == "RUT":
            self._validate_rut(document, result)
        elif document_type == "NIT":
            self._validate_nit(document, result)
        else:
            # Para outros tipos de documento, apenas validação básica
            if not re.match(r"^[a-zA-Z0-9\-/.]+$", document):
                result.add_error("Document must contain only letters, numbers, hyphens, dots and slashes", "document")

    # [VALIDATE CNPJ]
    # [Valida formato do CNPJ brasileiro]
    # [ENTRADA: cnpj - CNPJ a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se CNPJ inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_cnpj(self, cnpj: str, result: ValidationResult):
        # Remove caracteres especiais
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        
        if len(cnpj) != 14:
            result.add_error("CNPJ must have exactly 14 digits", "document")
            return
        
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            result.add_error("CNPJ cannot have all digits the same", "document")
            return

    # [VALIDATE CUIT]
    # [Valida formato do CUIT argentino]
    # [ENTRADA: cuit - CUIT a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se CUIT inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_cuit(self, cuit: str, result: ValidationResult):
        # CUIT format: XX-XXXXXXXX-X (11 dígitos)
        cuit = re.sub(r'[^0-9]', '', cuit)

        if len(cuit) != 11:
            result.add_error("CUIT must have exactly 11 digits", "document")
            return

        if cuit == cuit[0] * 11:
            result.add_error("CUIT cannot have all digits the same", "document")

    # [VALIDATE RUC]
    # [Valida formato do RUC paraguaio]
    # [ENTRADA: ruc - RUC a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se RUC inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_ruc(self, ruc: str, result: ValidationResult):
        # RUC format: Paraguai - geralmente 6-8 dígitos seguidos de -X
        ruc = re.sub(r'[^0-9]', '', ruc)

        if len(ruc) < 6 or len(ruc) > 9:
            result.add_error("RUC must have between 6 and 9 digits", "document")

    # [VALIDATE RUT]
    # [Valida formato do RUT chileno/uruguaio]
    # [ENTRADA: rut - RUT a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se RUT inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_rut(self, rut: str, result: ValidationResult):
        # RUT format: Chile/Uruguai - 8-9 dígitos (pode conter K)
        rut = re.sub(r'[^0-9kK]', '', rut)

        if len(rut) < 8 or len(rut) > 9:
            result.add_error("RUT must have between 8 and 9 characters", "document")

    # [VALIDATE NIT]
    # [Valida formato do NIT boliviano]
    # [ENTRADA: nit - NIT a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se NIT inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_nit(self, nit: str, result: ValidationResult):
        # NIT format: Bolívia - geralmente 7-10 dígitos
        nit = re.sub(r'[^0-9]', '', nit)

        if len(nit) < 7 or len(nit) > 10:
            result.add_error("NIT must have between 7 and 10 digits", "document")

    # [VALIDATE EMAIL]
    # [Valida formato do email]
    # [ENTRADA: email - email a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se email inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_email(self, email: str, result: ValidationResult):
        if not email or len(email.strip()) < 5:
            result.add_error("Email must be at least 5 characters long", "email")
            return
        
        if len(email) > 100:
            result.add_error("Email must be less than 100 characters", "email")
            return
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            result.add_error("Email must be a valid email address", "email")

    # [VALIDATE PHONE]
    # [Valida formato do telefone]
    # [ENTRADA: phone - telefone a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se telefone inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_phone(self, phone: str, result: ValidationResult):
        if not phone or len(phone.strip()) < 8:
            result.add_error("Phone must be at least 8 characters long", "phone")
            return
        
        if len(phone) > 20:
            result.add_error("Phone must be less than 20 characters", "phone")
            return
        
        # Aceita vários formatos de telefone
        phone_pattern = r'^[\+]?[\d\s\-\(\)\.]{8,20}$'
        if not re.match(phone_pattern, phone):
            result.add_error("Phone must be a valid phone number", "phone")

    # [VALIDATE CITY]
    # [Valida cidade - tamanho, caracteres permitidos]
    # [ENTRADA: city - cidade a ser validada, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se cidade inválida]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_city(self, city: str, result: ValidationResult):
        if not city or len(city.strip()) < 2:
            result.add_error("City must be at least 2 characters long", "city")
        
        if len(city) > 100:
            result.add_error("City must be less than 100 characters", "city")
        
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-'\.]+$", city):
            result.add_error("City must contain only letters, spaces, hyphens, apostrophes and dots", "city")
import re
from typing import List
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.user import UserCreate


# [USER VALIDATOR]
# [Validador customizado para dados de usuário com regras específicas do negócio]
# [ENTRADA: data - UserCreate com dados do usuário]
# [SAIDA: ValidationResult com resultado da validação]
# [DEPENDENCIAS: BaseValidator, ValidationResult, re]
class UserValidator(BaseValidator):

    # [VALIDATE]
    # [Método principal que executa todas as validações dos campos do usuário]
    # [ENTRADA: data - UserCreate com dados do usuário]
    # [SAIDA: ValidationResult - resultado consolidado de todas as validações]
    # [DEPENDENCIAS: ValidationResult, métodos privados de validação]
    def validate(self, data: UserCreate) -> ValidationResult:
        result = ValidationResult()
        
        self._validate_nationality(data.nationality, result)
        self._validate_document_type(data.document_type, result)
        self._validate_document(data.document, data.document_type, result)
        self._validate_name(data.name, result)
        self._validate_email_domain(data.email, result)
        self._validate_phone(data.phone, result)
        self._validate_password_strength(data.password, result)
        
        return result
    
    # [VALIDATE NATIONALITY]
    # [Valida nacionalidade - deve ser um dos valores permitidos]
    # [ENTRADA: nationality - nacionalidade a ser validada, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_nationality(self, nationality: str, result: ValidationResult):
        valid_nationalities = [
            "Brasileira", "Americana", "Canadense", "Argentina", "Chilena", "Colombiana",
            "Peruana", "Uruguaia", "Paraguaia", "Boliviana", "Venezuelana", "Equatoriana",
            "Francesa", "Alemã", "Italiana", "Espanhola", "Portuguesa", "Inglesa",
            "Suíça", "Holandesa", "Belga", "Austríaca", "Sueca", "Norueguesa",
            "Dinamarquesa", "Finlandesa", "Japonesa", "Chinesa", "Coreana", "Indiana",
            "Australiana", "Nova Zelandesa", "Mexicana", "Cubana"
        ]
        
        if nationality not in valid_nationalities:
            result.add_error(f"Nationality must be one of: {', '.join(valid_nationalities)}", "nationality")

    # [VALIDATE DOCUMENT TYPE]
    # [Valida tipo do documento - deve ser um dos valores permitidos]
    # [ENTRADA: document_type - tipo do documento, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se tipo inválido]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_document_type(self, document_type: str, result: ValidationResult):
        valid_types = ["CPF", "RG", "CNH", "PASSPORT", "OTHER"]
        
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

        if document_type == "CPF":
            self._validate_cpf(document, result)
        elif document_type == "RG":
            self._validate_rg(document, result)
        elif document_type == "CNH":
            self._validate_cnh(document, result)
        elif document_type == "PASSPORT":
            self._validate_passport(document, result)
        else:
            # Para outros tipos de documento, apenas validação básica
            if not re.match(r"^[a-zA-Z0-9\-/.]+$", document):
                result.add_error("Document must contain only letters, numbers, hyphens, dots and slashes", "document")

    # [VALIDATE CPF]
    # [Valida formato do CPF brasileiro]
    # [ENTRADA: cpf - CPF a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se CPF inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_cpf(self, cpf: str, result: ValidationResult):
        # Remove caracteres especiais
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf) != 11:
            result.add_error("CPF must have exactly 11 digits", "document")
            return
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            result.add_error("CPF cannot have all digits the same", "document")
            return

    # [VALIDATE RG]
    # [Valida formato do RG brasileiro]
    # [ENTRADA: rg - RG a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se RG inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_rg(self, rg: str, result: ValidationResult):
        # RG pode ter formato variado, validação básica
        rg = re.sub(r'[^0-9xX]', '', rg)
        
        if len(rg) < 7 or len(rg) > 10:
            result.add_error("RG must have between 7 and 10 characters", "document")

    # [VALIDATE CNH]
    # [Valida formato da CNH brasileira]
    # [ENTRADA: cnh - CNH a ser validada, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se CNH inválida]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_cnh(self, cnh: str, result: ValidationResult):
        # Remove caracteres especiais
        cnh = re.sub(r'[^0-9]', '', cnh)
        
        if len(cnh) != 11:
            result.add_error("CNH must have exactly 11 digits", "document")

    # [VALIDATE PASSPORT]
    # [Valida formato do passaporte]
    # [ENTRADA: passport - passaporte a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se passaporte inválido]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_passport(self, passport: str, result: ValidationResult):
        # Passaporte pode ter formato variado dependendo do país
        if not re.match(r'^[A-Z0-9]{6,12}$', passport.upper()):
            result.add_error("Passport must be 6-12 alphanumeric characters", "document")
    
    # [VALIDATE NAME]
    # [Valida nome do usuário - tamanho, caracteres permitidos]
    # [ENTRADA: name - nome a ser validado, result - ValidationResult para adicionar erros]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_name(self, name: str, result: ValidationResult):
        if not name or len(name.strip()) < 2:
            result.add_error("Name must be at least 2 characters long", "name")
        
        if len(name) > 100:
            result.add_error("Name must be less than 100 characters", "name")
        
        if not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", name):
            result.add_error("Name must contain only letters and spaces", "name")
    
    # [VALIDATE EMAIL DOMAIN]
    # [Valida formato do domínio do email - adicional à validação do Pydantic]
    # [ENTRADA: email - email a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se domínio inválido]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_email_domain(self, email: str, result: ValidationResult):
        if "@" in email:
            domain = email.split("@")[1]
            if len(domain.split(".")) < 2:
                result.add_error("Invalid email domain format", "email")

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
    
    # [VALIDATE PASSWORD STRENGTH]
    # [Valida força da senha - tamanho, maiúscula, minúscula, número e caractere especial]
    # [ENTRADA: password - senha a ser validada, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se senha fraca]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_password_strength(self, password: str, result: ValidationResult):
        if len(password) < 8:
            result.add_error("Password must be at least 8 characters long", "password")
        
        if len(password) > 128:
            result.add_error("Password must be less than 128 characters", "password")
        
        if not re.search(r'[A-Z]', password):
            result.add_error("Password must contain at least one uppercase letter", "password")
        
        if not re.search(r'[a-z]', password):
            result.add_error("Password must contain at least one lowercase letter", "password")
        
        if not re.search(r'\d', password):
            result.add_error("Password must contain at least one number", "password")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            result.add_error("Password must contain at least one special character", "password")
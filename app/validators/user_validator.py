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

        self._validate_name(data.name, result)
        self._validate_email_domain(data.email, result)
        self._validate_phone(data.phone, result)
        self._validate_password_strength(data.password, result)

        return result
    
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
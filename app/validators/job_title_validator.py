import re
from typing import List
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
        self._validate_department(data.department, result)
        self._validate_seniority_level(data.seniority_level, result)
        
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
    
    # [VALIDATE DEPARTMENT]
    # [Valida departamento - tamanho, caracteres permitidos]
    # [ENTRADA: department - departamento a ser validado, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se encontrados]
    # [DEPENDENCIAS: re, ValidationResult.add_error]
    def _validate_department(self, department: str, result: ValidationResult):
        if not department or len(department.strip()) < 2:
            result.add_error("Department must be at least 2 characters long", "department")
        
        if len(department) > 50:
            result.add_error("Department must be less than 50 characters", "department")
        
        # List of valid departments (hospital and business departments)
        valid_departments = [
            "Recursos Humanos", "RH", "Tecnologia", "TI", "Vendas", "Marketing",
            "Financeiro", "Contabilidade", "Operações", "Produção", "Qualidade",
            "Jurídico", "Administrativo", "Diretoria", "Gerência", "Suporte",
            "Atendimento", "Logística", "Compras", "Engenharia", "Pesquisa",
            "Desenvolvimento", "Design", "Comunicação", "Comercial",
            "Emergência", "UTI", "CTI", "Centro Cirúrgico", "Bloco Cirúrgico",
            "Enfermaria", "Pediatria", "Maternidade", "Obstetrícia", "Ginecologia",
            "Cardiologia", "Neurologia", "Ortopedia", "Oncologia", "Radiologia",
            "Laboratório", "Farmácia", "Fisioterapia", "Nutrição", "Psicologia",
            "Medicina Interna", "Clínica Médica", "Cirurgia Geral", "Anestesiologia",
            "Patologia", "Hematologia", "Nefrologia", "Pneumologia", "Dermatologia",
            "Oftalmologia", "Otorrinolaringologia", "Urologia", "Psiquiatria",
            "Geriatria", "Infectologia", "Endocrinologia", "Gastroenterologia",
            "Reumatologia", "Pronto Socorro", "Ambulatório", "Internação",
            "Centro de Material", "Esterilização", "Limpeza", "Segurança",
            "Manutenção", "Hotelaria", "Recepção", "Faturamento"
        ]
        
        if department not in valid_departments:
            result.add_error(f"Department must be one of: {', '.join(valid_departments)}", "department")

    # [VALIDATE SENIORITY LEVEL]
    # [Valida nível de senioridade - deve ser um dos valores permitidos]
    # [ENTRADA: seniority_level - nível de senioridade, result - ValidationResult]
    # [SAIDA: None - adiciona erros ao result se nível inválido]
    # [DEPENDENCIAS: ValidationResult.add_error]
    def _validate_seniority_level(self, seniority_level: str, result: ValidationResult):
        valid_levels = [
            "Estagiário", "Trainee", "Junior", "Pleno", "Senior",
            "Especialista", "Coordenador", "Supervisor", "Gerente",
            "Diretor", "Vice-Presidente", "Presidente", "CEO",
            "I", "II", "III", "1", "2", "3"
        ]

        if seniority_level not in valid_levels:
            result.add_error(f"Seniority level must be one of: {', '.join(valid_levels)}", "seniority_level")

        if len(seniority_level) > 20:
            result.add_error("Seniority level must be less than 20 characters", "seniority_level")
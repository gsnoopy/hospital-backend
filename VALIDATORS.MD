# Validators Documentation

Este documento descreve todas as validações implementadas no backend para cada entidade do sistema. Use este guia para implementar validações no frontend e garantir consistência entre as camadas.

---

## 📋 Índice

1. [Hospital](#hospital)
2. [User](#user)
3. [Job Title](#job-title)
4. [Category](#category)
5. [SubCategory](#subcategory)
6. [Catalog](#catalog)
7. [Item](#item)
8. [Supplier](#supplier)
9. [Public Acquisition](#public-acquisition)

---

## 🏥 Hospital

### Campo: `name`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 200 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `&`, `.`, `/`, `(`, `)`, `-`
- **Mensagens de erro**:
  - `"Name must be at least 2 characters long"`
  - `"Name must be less than 200 characters"`
  - `"Name must contain only letters, numbers, spaces and basic punctuation (&./()-)"`

### Campo: `nationality`
- **Obrigatório**: Sim
- **Tipo**: String (Enum)
- **Valores aceitos** (Países do Mercosul e associados):
  - `Brasileira`
  - `Argentina`
  - `Paraguaia`
  - `Uruguaia`
  - `Boliviana`
  - `Chilena`
- **Mensagem de erro**:
  - `"Nationality must be one of: Brasileira, Argentina, Paraguaia, Uruguaia, Boliviana, Chilena"`

### Campo: `document_type`
- **Obrigatório**: Sim
- **Tipo**: String (Enum)
- **Valores aceitos** (Documentos de empresas do Mercosul):
  - `CNPJ` - Brasil (Cadastro Nacional da Pessoa Jurídica)
  - `CUIT` - Argentina (Clave Única de Identificación Tributaria)
  - `RUC` - Paraguai (Registro Único del Contribuyente)
  - `RUT` - Chile/Uruguai (Rol Único Tributario)
  - `NIT` - Bolívia (Número de Identificación Tributaria)
  - `OTHER` - Outros tipos
- **Mensagem de erro**:
  - `"Document type must be one of: CNPJ, CUIT, RUC, RUT, NIT, OTHER"`

### Campo: `document`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras gerais**:
  - Mínimo: 5 caracteres
  - Máximo: 30 caracteres
- **Regras específicas por tipo**:

  **CNPJ** (Brasil):
  - Exatamente 14 dígitos (após remover caracteres especiais)
  - Não pode ter todos os dígitos iguais
  - Formato aceito: `XX.XXX.XXX/XXXX-XX` ou apenas números

  **CUIT** (Argentina):
  - Exatamente 11 dígitos (após remover caracteres especiais)
  - Não pode ter todos os dígitos iguais
  - Formato aceito: `XX-XXXXXXXX-X` ou apenas números

  **RUC** (Paraguai):
  - Entre 6 e 9 dígitos

  **RUT** (Chile/Uruguai):
  - Entre 8 e 9 caracteres
  - Pode conter a letra K no final

  **NIT** (Bolívia):
  - Entre 7 e 10 dígitos

  **Outros tipos**:
  - Caracteres permitidos: Letras, números, hífens, pontos, barras
- **Mensagens de erro**:
  - `"Document must be at least 5 characters long"`
  - `"Document must be less than 30 characters"`
  - `"CNPJ must have exactly 14 digits"`
  - `"CNPJ cannot have all digits the same"`
  - `"CUIT must have exactly 11 digits"`
  - `"CUIT cannot have all digits the same"`
  - `"RUC must have between 6 and 9 digits"`
  - `"RUT must have between 8 and 9 characters"`
  - `"NIT must have between 7 and 10 digits"`
  - `"Document must contain only letters, numbers, hyphens, dots and slashes"`

### Campo: `email`
- **Obrigatório**: Sim
- **Tipo**: Email
- **Regras**:
  - Mínimo: 5 caracteres
  - Máximo: 100 caracteres
  - Deve ser um email válido (formato: `usuario@dominio.com`)
- **Mensagens de erro**:
  - `"Email must be at least 5 characters long"`
  - `"Email must be less than 100 characters"`
  - `"Email must be a valid email address"`

### Campo: `phone`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 8 caracteres
  - Máximo: 20 caracteres
  - Formato flexível: aceita números, espaços, hífens, parênteses, pontos, `+`
  - Padrão aceito: `^[\+]?[\d\s\-\(\)\.]{8,20}$`
- **Mensagens de erro**:
  - `"Phone must be at least 8 characters long"`
  - `"Phone must be less than 20 characters"`
  - `"Phone must be a valid phone number"`

### Campo: `city`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 100 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), espaços, hífens, apóstrofos, pontos
- **Mensagens de erro**:
  - `"City must be at least 2 characters long"`
  - `"City must be less than 100 characters"`
  - `"City must contain only letters, spaces, hyphens, apostrophes and dots"`

---

## 👤 User

### Campo: `name`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 100 caracteres
  - Caracteres permitidos: Apenas letras (a-z, A-Z, À-ÿ) e espaços
- **Mensagens de erro**:
  - `"Name must be at least 2 characters long"`
  - `"Name must be less than 100 characters"`
  - `"Name must contain only letters and spaces"`

### Campo: `email`
- **Obrigatório**: Sim
- **Tipo**: Email
- **Regras**:
  - Deve ser um email válido
  - Domínio deve ter pelo menos um ponto (ex: `user@example.com`)
- **Mensagem de erro**:
  - `"Invalid email domain format"`

### Campo: `phone`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 8 caracteres
  - Máximo: 20 caracteres
  - Formato flexível: aceita números, espaços, hífens, parênteses, pontos, `+`
  - Padrão: `^[\+]?[\d\s\-\(\)\.]{8,20}$`
- **Mensagens de erro**:
  - `"Phone must be at least 8 characters long"`
  - `"Phone must be less than 20 characters"`
  - `"Phone must be a valid phone number"`

### Campo: `password`
- **Obrigatório**: Sim (apenas na criação)
- **Tipo**: String
- **Regras**:
  - Mínimo: 8 caracteres
  - Máximo: 128 caracteres
  - Deve conter pelo menos:
    - Uma letra maiúscula (A-Z)
    - Uma letra minúscula (a-z)
    - Um número (0-9)
    - Um caractere especial (`!@#$%^&*(),.?":{}|<>`)
- **Mensagens de erro**:
  - `"Password must be at least 8 characters long"`
  - `"Password must be less than 128 characters"`
  - `"Password must contain at least one uppercase letter"`
  - `"Password must contain at least one lowercase letter"`
  - `"Password must contain at least one number"`
  - `"Password must contain at least one special character"`

---

## 💼 Job Title

### Campo: `title`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 100 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `&`, `.`, `/`, `(`, `)`, `-`
- **Mensagens de erro**:
  - `"Title must be at least 2 characters long"`
  - `"Title must be less than 100 characters"`
  - `"Title must contain only letters, numbers, spaces and basic punctuation (&./()-)"`

---

## 📁 Category

### Campo: `name`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 100 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`
- **Mensagens de erro**:
  - `"Category name must be at least 2 characters long"`
  - `"Category name must be less than 100 characters"`
  - `"Category name must contain only letters, numbers, spaces, hyphens, ampersands, and parentheses"`

### Campo: `description`
- **Obrigatório**: Não
- **Tipo**: String
- **Regras**:
  - Máximo: 500 caracteres
- **Mensagem de erro**:
  - `"Category description must be less than 500 characters"`

---

## 📂 SubCategory

### Campo: `name`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 100 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`
- **Mensagens de erro**:
  - `"SubCategory name must be at least 2 characters long"`
  - `"SubCategory name must be less than 100 characters"`
  - `"SubCategory name must contain only letters, numbers, spaces, hyphens, ampersands, and parentheses"`

### Campo: `description`
- **Obrigatório**: Não
- **Tipo**: String
- **Regras**:
  - Máximo: 500 caracteres
- **Mensagem de erro**:
  - `"SubCategory description must be less than 500 characters"`

### Campo: `category_id`
- **Obrigatório**: Sim
- **Tipo**: UUID
- **Regras**:
  - Deve ser um UUID válido
  - A categoria referenciada deve existir no sistema
- **Mensagem de erro**:
  - `"Category ID is required"`
  - `"Category with ID '{id}' not found"` (verificado no service)

---

## 📚 Catalog

### Campo: `name`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 200 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`, `,`, `/`, `+`
- **Mensagens de erro**:
  - `"Catalog name must be at least 2 characters long"`
  - `"Catalog name must be less than 200 characters"`
  - `"Catalog name contains invalid characters"`

### Campo: `description`
- **Obrigatório**: Não
- **Tipo**: String
- **Regras**:
  - Máximo: 500 caracteres
- **Mensagem de erro**:
  - `"Catalog description must be less than 500 characters"`

### Campo: `full_description`
- **Obrigatório**: Não
- **Tipo**: Text
- **Regras**:
  - Máximo: 2000 caracteres
- **Mensagem de erro**:
  - `"Catalog full description must be less than 2000 characters"`

### Campo: `presentation`
- **Obrigatório**: Não
- **Tipo**: String
- **Regras**:
  - Máximo: 100 caracteres
- **Mensagem de erro**:
  - `"Catalog presentation must be less than 100 characters"`

### Campo: `similar_names`
- **Obrigatório**: Não
- **Tipo**: Array de Strings
- **Regras**:
  - Máximo: 20 itens no array
  - Cada item deve ter:
    - Mínimo: 2 caracteres
    - Máximo: 200 caracteres
    - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`, `,`, `/`, `+`
- **Mensagens de erro**:
  - `"Similar names must be a list"`
  - `"Similar names list must have at most 20 items"`
  - `"Similar name at index {idx} must be a string"`
  - `"Similar name at index {idx} must be at least 2 characters"`
  - `"Similar name at index {idx} must be less than 200 characters"`
  - `"Similar name at index {idx} contains invalid characters"`

---

## 📦 Item

### Campo: `name`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 200 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`, `,`, `/`, `+`
- **Mensagens de erro**:
  - `"Item name must be at least 2 characters long"`
  - `"Item name must be less than 200 characters"`
  - `"Item name contains invalid characters"`

### Campo: `similar_names`
- **Obrigatório**: Não
- **Tipo**: Array de Strings
- **Regras**:
  - Máximo: 20 itens no array
  - Cada item deve ter:
    - Mínimo: 2 caracteres
    - Máximo: 200 caracteres
    - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`, `,`, `/`, `+`
- **Mensagens de erro**:
  - `"Similar names must be a list"`
  - `"Similar names list must have at most 20 items"`
  - `"Similar name at index {idx} must be a string"`
  - `"Similar name at index {idx} must be at least 2 characters"`
  - `"Similar name at index {idx} must be less than 200 characters"`
  - `"Similar name at index {idx} contains invalid characters"`

### Campo: `description`
- **Obrigatório**: Não
- **Tipo**: String
- **Regras**:
  - Máximo: 500 caracteres
- **Mensagem de erro**:
  - `"Item description must be less than 500 characters"`

### Campo: `full_description`
- **Obrigatório**: Não
- **Tipo**: Text
- **Regras**:
  - Máximo: 2000 caracteres
- **Mensagem de erro**:
  - `"Item full description must be less than 2000 characters"`

### Campo: `internal_code`
- **Obrigatório**: Não
- **Tipo**: String
- **Regras**:
  - Máximo: 50 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z), números (0-9), hífens (`-`), underscores (`_`)
- **Mensagens de erro**:
  - `"Internal code must be less than 50 characters"`
  - `"Internal code must contain only letters, numbers, hyphens and underscores"`

### Campo: `presentation`
- **Obrigatório**: Não
- **Tipo**: String
- **Regras**:
  - Máximo: 100 caracteres
- **Mensagem de erro**:
  - `"Item presentation must be less than 100 characters"`

### Campo: `sample`
- **Obrigatório**: Não
- **Tipo**: Integer
- **Regras**:
  - Deve ser um número positivo (>= 0)
- **Mensagem de erro**:
  - `"Sample quantity must be a positive number"`

### Campo: `has_catalog`
- **Obrigatório**: Não
- **Tipo**: Boolean
- **Valor padrão**: `false`
- **Regras**:
  - Deve ser `true` ou `false`

### Campo: `subcategory_id`
- **Obrigatório**: Sim
- **Tipo**: UUID
- **Regras**:
  - Deve ser um UUID válido
  - A subcategoria referenciada deve existir no sistema
- **Mensagens de erro**:
  - `"SubCategory with ID '{id}' not found"` (verificado no service)

---

## 🏭 Supplier

### Campo: `name`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 200 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`, `,`, `/`
- **Mensagens de erro**:
  - `"Supplier name must be at least 2 characters long"`
  - `"Supplier name must be less than 200 characters"`
  - `"Supplier name contains invalid characters"`

### Campo: `document_type`
- **Obrigatório**: Sim
- **Tipo**: String (Enum)
- **Valores aceitos**:
  - `CPF` - Brasil (Cadastro de Pessoa Física)
  - `CNPJ` - Brasil (Cadastro Nacional da Pessoa Jurídica)
  - `DNI` - Argentina (Documento Nacional de Identidad)
  - `CUIT` - Argentina (Clave Única de Identificación Tributaria)
  - `CUIL` - Argentina (Código Único de Identificación Laboral)
  - `CI` - Paraguai (Cédula de Identidad)
  - `RUC` - Paraguai (Registro Único del Contribuyente)
- **Mensagem de erro**:
  - `"Document type must be one of: CPF, CNPJ, DNI, CUIT, CUIL, CI, RUC"`

### Campo: `document`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras específicas por tipo**:

  **CPF** (Brasil - Pessoa Física):
  - Exatamente 11 dígitos (após remover caracteres especiais)
  - Formato aceito: `XXX.XXX.XXX-XX` ou apenas números

  **CNPJ** (Brasil - Pessoa Jurídica):
  - Exatamente 14 dígitos (após remover caracteres especiais)
  - Formato aceito: `XX.XXX.XXX/XXXX-XX` ou apenas números

  **DNI** (Argentina - Pessoa Física):
  - Entre 7 e 8 dígitos (após remover caracteres especiais)

  **CUIT** (Argentina - Pessoa Jurídica):
  - Exatamente 11 dígitos (após remover caracteres especiais)
  - Formato aceito: `XX-XXXXXXXX-X` ou apenas números

  **CUIL** (Argentina - Pessoa Física):
  - Exatamente 11 dígitos (após remover caracteres especiais)
  - Formato aceito: `XX-XXXXXXXX-X` ou apenas números

  **CI** (Paraguai - Pessoa Física):
  - Entre 6 e 8 dígitos (após remover caracteres especiais)

  **RUC** (Paraguai - Pessoa Jurídica):
  - Entre 6 e 9 dígitos (após remover caracteres especiais)

- **Mensagens de erro**:
  - `"Document is required"`
  - `"CPF must have 11 digits"`
  - `"CNPJ must have 14 digits"`
  - `"DNI must have 7 or 8 digits"`
  - `"CUIT must have 11 digits"`
  - `"CUIL must have 11 digits"`
  - `"CI must have 6 to 8 digits"`
  - `"RUC must have 6 to 9 digits"`

### Campo: `email`
- **Obrigatório**: Sim
- **Tipo**: Email
- **Regras**:
  - Máximo: 255 caracteres
  - Deve ser um email válido (formato: `usuario@dominio.com`)
- **Mensagens de erro**:
  - `"Email is required"`
  - `"Invalid email format"`
  - `"Email must be less than 255 characters"`

### Campo: `phone`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Entre 10 e 11 dígitos (após remover caracteres especiais)
  - Aceita celular ou fixo com DDD
- **Mensagens de erro**:
  - `"Phone is required"`
  - `"Phone must have 10 or 11 digits"`

---

## 📋 Public Acquisition

### Campo: `code`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 2 caracteres
  - Máximo: 100 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z), números (0-9), espaços, `-`, `/`, `_`
- **Mensagens de erro**:
  - `"Public acquisition code must be at least 2 characters long"`
  - `"Public acquisition code must be less than 100 characters"`
  - `"Public acquisition code contains invalid characters"`

### Campo: `title`
- **Obrigatório**: Sim
- **Tipo**: String
- **Regras**:
  - Mínimo: 5 caracteres
  - Máximo: 500 caracteres
  - Caracteres permitidos: Letras (a-z, A-Z, À-ÿ), números (0-9), espaços, `-`, `&`, `(`, `)`, `.`, `,`, `/`, `:`, `;`, `+`, `#`, `@`
- **Mensagens de erro**:
  - `"Public acquisition title must be at least 5 characters long"`
  - `"Public acquisition title must be less than 500 characters"`
  - `"Public acquisition title contains invalid characters"`

---

## 🔄 Validações Adicionais (Service Layer)

Além das validações de formato, o backend também verifica **regras de negócio** na camada de serviço:

### Unicidade (Duplicatas)

As seguintes entidades verificam se já existe um registro com o mesmo valor:

**Hospital**:
- `name`: Nome único
- `document`: Documento único
- `email`: Email único
- `phone`: Telefone único

**User**:
- `email`: Email único
- `phone`: Telefone único

**Job Title**:
- `title`: Título único

**Category**:
- `name`: Nome único

**SubCategory**:
- `name`: Nome único

**Catalog**:
- `name`: Nome único

**Item**:
- `internal_code`: Código interno único (se fornecido)

**Supplier**:
- `document`: Documento único dentro do hospital
- `email`: Email único dentro do hospital

**Public Acquisition**:
- `code`: Código único dentro do hospital

### Existência de Relacionamentos

**User**:
- `role_id`: Role deve existir
- `job_title_id`: JobTitle deve existir (se fornecido)
- `hospital_id`: Hospital deve existir (se fornecido)

**SubCategory**:
- `category_id`: Category deve existir

**Item**:
- `subcategory_id`: SubCategory deve existir

---

## 🌎 Documentos por País

### Brasil 🇧🇷
**Pessoas**:
- CPF (11 dígitos)
- RG (7-10 caracteres)
- CNH (11 dígitos)

**Empresas**:
- CNPJ (14 dígitos)

### Argentina 🇦🇷
**Pessoas**:
- DNI (7-8 dígitos)
- CUIL (11 dígitos)

**Empresas**:
- CUIT (11 dígitos)

### Paraguai 🇵🇾
**Pessoas**:
- CI (6-9 dígitos)

**Empresas**:
- RUC (6-9 dígitos)

### Uruguai 🇺🇾
**Pessoas**:
- CI (6-9 dígitos)

**Empresas**:
- RUT (8-9 caracteres)

### Chile 🇨🇱
**Pessoas**:
- RUT (8-9 caracteres, pode ter K)

**Empresas**:
- RUT (8-9 caracteres, pode ter K)

### Bolívia 🇧🇴
**Pessoas**:
- CI (6-9 dígitos)

**Empresas**:
- NIT (7-10 dígitos)

---

**Última atualização**: 2025-10-19
**Versão do Backend**: 1.0.0
**Região**: Mercosul (Brasil, Argentina, Paraguai, Uruguai, Chile, Bolívia)

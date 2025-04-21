# ftc-video-to-zip-service

Repositório de microserviço de conversão de vídeo para projeto do módulo final da FIAP

# Arquitetura

## Visão Geral

Este projeto é uma plataforma modular e escalável de processamento de vídeo construída com FastAPI, seguindo a Arquitetura Limpa e os princípios SOLID. O sistema é projetado para manutenibilidade, testabilidade e extensibilidade, suportando gerenciamento de usuários, upload de vídeo, extração de quadros e armazenamento em nuvem.

## Camadas Arquiteturais

### 1. Camada de API (Frameworks & Drivers)

- **Localização:** `src/api/`
- **Responsabilidade:** Expõe endpoints HTTP usando FastAPI. Lida com validação de requisições, autenticação e delega a lógica de negócios para a camada de serviços.
- **Estrutura:**
  - `app.py`: Instanciação do app FastAPI e inclusão de rotas.
  - `v1/`: Endpoints de API versionados (`videos.py`, `users.py`, `auth.py`), com validação de requisições em `v1/validations/`.

### 2. Camada de Serviços (Casos de Uso)

- **Localização:** `src/services/`
- **Responsabilidade:** Contém a lógica de negócios e orquestra fluxos de trabalho. Os serviços são desacoplados de frameworks e infraestrutura, dependendo apenas de interfaces.
- **Serviços Principais:**
  - `UserService`, `AuthService`: Gerenciamento de usuários e autenticação.
  - `VideoService`: Upload de vídeo, extração de quadros e orquestração.
  - `TempFileService`, `ZipService`, `VideoFrameExtractor`: Utilitários de suporte.
  - `NotificationService`: Lida com notificações por e-mail e outras para os usuários.

### 3. Camada de Repositório (Adaptadores de Interface)

- **Localização:** `src/repositories/`
- **Responsabilidade:** Implementa a lógica de acesso a dados, traduzindo entre modelos de domínio e modelos de banco de dados. Depende de interfaces definidas em `db/postgresql/interfaces/`.
- **Repositórios:** `UserRepository`, `VideoRepository`.

### 4. Camada de Infraestrutura

- **Localização:** `src/infrastructure/`
- **Responsabilidade:** Integra-se com sistemas externos (por exemplo, AWS S3 para armazenamento). Implementa interfaces definidas em `core/interfaces/`.
- **Exemplo:** `S3StorageService` em `storage/`.

### 5. Camada Central (Entidades, Interfaces, Configuração)

- **Localização:** `src/core/`
- **Responsabilidade:** Contém abstrações centrais, interfaces, segurança e configuração.
- **Componentes:**
  - `interfaces/`: Classes base abstratas para serviços (por exemplo, `StorageServiceInterface`).
  - `settings.py`: Configuração centralizada.
  - `security.py`: Utilitários de segurança (JWT, hash de senhas).
  - `dependency_injection.py`: Contêiner de injeção de dependência.

### 6. Camada de Banco de Dados

- **Localização:** `src/db/`
- **Responsabilidade:** Gerencia conexões e modelos de banco de dados.
- **Estrutura:**
  - `postgresql/database.py`: Gerenciamento de sessão do DB.
  - `postgresql/models/`: Modelos ORM do SQLAlchemy.
  - `postgresql/interfaces/`: Interfaces de repositório.

### 7. Esquemas (DTOs)

- **Localização:** `src/schemas/`
- **Responsabilidade:** Modelos Pydantic para validação de requisições/respostas e transferência de dados.

### 8. Templates

- **Localização:** `src/templates/`
- **Responsabilidade:** Contém HTML ou outros templates usados para notificações por e-mail ou outras saídas formatadas.
- **Exemplo:** `email_template.html` para envio de e-mails formatados.

## Princípios Arquiteturais Chave

### Arquitetura Limpa

- **Regra de Dependência:** Todas as dependências apontam para dentro. A lógica de negócios central é independente de frameworks e infraestrutura.
- **Separação de Preocupações:** Cada camada tem uma responsabilidade clara e focada.
- **Testabilidade:** A lógica de negócios pode ser testada independentemente do framework web ou banco de dados.

### Princípios SOLID

- **Responsabilidade Única:** Cada classe/serviço tem uma responsabilidade.
- **Aberto/Fechado:** Interfaces e injeção de dependência permitem fácil extensão.
- **Substituição de Liskov:** Implementações podem ser trocadas sem quebrar contratos.
- **Segregação de Interface:** Interfaces são focadas e não excessivamente amplas.
- **Inversão de Dependência:** Módulos de alto nível dependem de abstrações, não de implementações concretas.

## Fluxo de Dados

1. **Requisição** atinge o endpoint da API (rota FastAPI).
2. **Validação** é realizada usando esquemas Pydantic.
3. **Camada de Serviços** processa a requisição, orquestrando a lógica de negócios.
4. **Repositórios** lidam com a persistência de dados, abstraindo o banco de dados.
5. **Serviços de Infraestrutura** (por exemplo, S3) lidam com integrações externas.
6. **Resposta** é retornada ao cliente.

## Extensibilidade & Manutenibilidade

- **Adicionar novos backends de armazenamento:** Implemente uma nova classe em `infrastructure/storage/` e registre-a via injeção de dependência.
- **Adicionar novas versões da API:** Crie uma nova pasta sob `api/` (por exemplo, `v2/`).
- **Adicionar nova lógica de negócios:** Adicione novos serviços em `services/` e interfaces correspondentes.

## Segurança & Melhores Práticas

- **Autenticação:** Baseada em JWT, usando `fastapi-jwt-auth`.
- **Gerenciamento de Usuários:** Via `fastapi-users`.
- **Validação:** Modelos Pydantic para todas as entradas/saídas.
- **Tratamento de Erros:** Centralizado e consistente.
- **Configuração:** Centralizada em `core/settings.py`.

## Diagrama Resumo (Textual)

```
[Camada de API] ---> [Camada de Serviços] ---> [Camada de Repositório] ---> [Banco de Dados]
      |                  |                    |
      |                  |                    +--> [Camada de Infraestrutura (por exemplo, S3)]
      |                  |
      |                  +--> [Camada Central (Interfaces, Segurança, Config)]
      |
      +--> [Esquemas (DTOs)]
```

## Configuração do Ambiente

1. Instale [Poetry](https://python-poetry.org/docs/) para gerenciamento de dependências.
2. Clone o repositório e navegue até a pasta do projeto.
3. Crie e ative um ambiente virtual:

   ```shell
   poetry shell
   ```

4. Instale as dependências:

   ```shell
   poetry install
   ```

   Para instalar apenas as dependências de produção, use:

   ```shell
   poetry install --no-dev
   ```

## Execução do Projeto

Utilize o Makefile fornecido para executar o projeto. Certifique-se de ter o Make instalado em seu sistema.

1. Para compilar e executar o projeto:

   ```shell
   make start-up
   ```

2. Para limpar os arquivos gerados durante a compilação:

   ```shell
   make clean-up
   ```

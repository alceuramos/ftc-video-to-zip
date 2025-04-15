# ftc-video-to-zip-service

Repositorio de microservico de conversão de vídeo para projeto do modulo final da fiap

# Architecture

## Overview

This project is a modular, scalable video processing platform built with FastAPI, following Clean Architecture and SOLID principles. The system is designed for maintainability, testability, and extensibility, supporting user management, video upload, frame extraction, and cloud storage.

## Architectural Layers

### 1. API Layer (Frameworks & Drivers)

- **Location:** `src/api/`
- **Responsibility:** Exposes HTTP endpoints using FastAPI. Handles request validation, authentication, and delegates business logic to the service layer.
- **Structure:**
  - `app.py`: FastAPI app instantiation and route inclusion.
  - `v1/`: Versioned API endpoints (`videos.py`, `users.py`, `auth.py`), with request validation in `v1/validations/`.

### 2. Service Layer (Use Cases)

- **Location:** `src/services/`
- **Responsibility:** Contains business logic and orchestrates workflows. Services are decoupled from frameworks and infrastructure, depending only on interfaces.
- **Key Services:**
  - `UserService`, `AuthService`: User management and authentication.
  - `VideoService`: Video upload, frame extraction, and orchestration.
  - `TempFileService`, `ZipService`, `VideoFrameExtractor`: Supporting utilities.
  - `NotificationService`: Handles email and other user notifications.

### 3. Repository Layer (Interface Adapters)

- **Location:** `src/repositories/`
- **Responsibility:** Implements data access logic, translating between domain models and database models. Depends on interfaces defined in `db/postgresql/interfaces/`.
- **Repositories:** `UserRepository`, `VideoRepository`.

### 4. Infrastructure Layer

- **Location:** `src/infrastructure/`
- **Responsibility:** Integrates with external systems (e.g., AWS S3 for storage). Implements interfaces defined in `core/interfaces/`.
- **Example:** `S3StorageService` in `storage/`.

### 5. Core Layer (Entities, Interfaces, Configuration)

- **Location:** `src/core/`
- **Responsibility:** Contains core abstractions, interfaces, security, and configuration.
- **Components:**
  - `interfaces/`: Abstract base classes for services (e.g., `StorageServiceInterface`).
  - `settings.py`: Centralized configuration.
  - `security.py`: Security utilities (JWT, password hashing).
  - `dependency_injection.py`: Dependency injection container.

### 6. Database Layer

- **Location:** `src/db/`
- **Responsibility:** Manages database connections and models.
- **Structure:**
  - `postgresql/database.py`: DB session management.
  - `postgresql/models/`: SQLAlchemy ORM models.
  - `postgresql/interfaces/`: Repository interfaces.

### 7. Schemas (DTOs)

- **Location:** `src/schemas/`
- **Responsibility:** Pydantic models for request/response validation and data transfer.

### 8. Templates

- **Location:** `src/templates/`
- **Responsibility:** Contains HTML or other templates used for email notifications or other templated outputs.
- **Example:** `email_template.html` for sending formatted emails.

## Key Architectural Principles

### Clean Architecture

- **Dependency Rule:** All dependencies point inward. The core business logic is independent of frameworks and infrastructure.
- **Separation of Concerns:** Each layer has a clear, focused responsibility.
- **Testability:** Business logic can be tested independently of the web framework or database.

### SOLID Principles

- **Single Responsibility:** Each class/service has one responsibility.
- **Open/Closed:** Interfaces and dependency injection allow for easy extension.
- **Liskov Substitution:** Implementations can be swapped without breaking contracts.
- **Interface Segregation:** Interfaces are focused and not overly broad.
- **Dependency Inversion:** High-level modules depend on abstractions, not concrete implementations.

## Data Flow

1. **Request** hits the API endpoint (FastAPI route).
2. **Validation** is performed using Pydantic schemas.
3. **Service Layer** processes the request, orchestrating business logic.
4. **Repositories** handle data persistence, abstracting the database.
5. **Infrastructure** services (e.g., S3) handle external integrations.
6. **Response** is returned to the client.

## Extensibility & Maintainability

- **Add new storage backends:** Implement a new class in `infrastructure/storage/` and register it via dependency injection.
- **Add new API versions:** Create a new folder under `api/` (e.g., `v2/`).
- **Add new business logic:** Add new services in `services/` and corresponding interfaces.

## Security & Best Practices

- **Authentication:** JWT-based, using `fastapi-jwt-auth`.
- **User Management:** Via `fastapi-users`.
- **Validation:** Pydantic models for all input/output.
- **Error Handling:** Centralized and consistent.
- **Configuration:** Centralized in `core/settings.py`.

## Summary Diagram (Textual)

```
[API Layer] ---> [Service Layer] ---> [Repository Layer] ---> [Database]
      |                  |                    |
      |                  |                    +--> [Infrastructure Layer (e.g., S3)]
      |                  |
      |                  +--> [Core Layer (Interfaces, Security, Config)]
      |
      +--> [Schemas (DTOs)]
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

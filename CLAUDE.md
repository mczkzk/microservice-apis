# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Python Development
- **Install dependencies**: `pipenv install` (in chapter directories)
- **Run services**: `pipenv run uvicorn orders.web.app:app --reload` (from chapter root)
- **Database migrations**: `pipenv run alembic upgrade head`
- **Run tests**: `pipenv run python test.py` (ch12)

### Docker & Containerization (ch13+)
- **Build image**: `docker build -t orders-service .`
- **Run with Docker Compose**: `docker-compose up`
- **Database migrations in Docker**: `docker-compose run --rm orders-service alembic upgrade head`

### API Testing & Validation
- **Mock API server**: `npx @stoplight/prism-cli mock oas.yaml` (requires `npm install`)
- **API testing with Dredd**: `npx dredd oas.yaml http://localhost:8000` (ch12)

### Code Quality
- **Format code**: `pipenv run black .` (available in most chapters)

## Architecture Overview

This is a **microservice APIs educational codebase** demonstrating clean architecture patterns:

### Core Architecture Patterns
- **Hexagonal Architecture**: Clear separation between domain, application, and infrastructure layers
- **Repository Pattern**: Data access abstraction (`OrdersRepository`)
- **Unit of Work Pattern**: Transaction management with context managers
- **Domain-Driven Design**: Rich domain entities with business logic
- **Dependency Injection**: Services receive dependencies through constructors

### Service Structure
```
orders/
├── orders_service/     # Domain & Business Logic
├── repository/         # Data Access Layer  
└── web/               # HTTP Presentation Layer
```

### Technology Stack by Chapter Evolution
- **Ch02-Ch06**: Basic FastAPI + Pydantic
- **Ch07**: SQLAlchemy + Alembic + Repository patterns
- **Ch08-Ch10**: GraphQL with Ariadne
- **Ch11**: JWT authentication with RS256
- **Ch12**: API testing (Dredd, Schemathesis)
- **Ch13**: Docker containerization
- **Ch14**: Kubernetes deployment
- **Appendix C**: Auth0 integration

### Key Dependencies
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM and database abstraction
- **Alembic**: Database migrations
- **Pydantic**: Data validation and serialization
- **PyJWT**: JWT token handling
- **PostgreSQL**: Production database (Docker)
- **Prism**: API mocking
- **Dredd**: API testing

### Authentication Patterns
- **JWT with RS256**: Public/private key pairs (`public_key.pem`, `private_key.pem`)
- **Auth0 integration**: External identity provider (appendix_c)
- **Middleware-based**: `AuthorizeRequestMiddleware` for request validation

### Database Patterns
- **Repository pattern**: Abstract data access with `OrdersRepository`
- **Unit of Work**: Manage transactions with context managers
- **Domain entities**: Rich objects with business logic (Order, OrderItem)
- **SQLAlchemy models**: ORM mapping in `repository/models.py`

### Service Communication
- **HTTP clients**: `requests` library for inter-service communication
- **OpenAPI specifications**: API-first development with `oas.yaml` files
- **GraphQL**: Alternative API pattern in products service

### Development Workflow
1. Navigate to specific chapter directory
2. Install dependencies with `pipenv install`
3. Run database migrations if needed
4. Start service with uvicorn
5. Use Prism for API mocking during development
6. Test with Dredd or custom test scripts
# Architecture Documentation

Technical architecture overview for LaTeXZen Scientific Paper Converter.

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Component Diagram](#component-diagram)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Database Schema](#database-schema)
7. [API Design](#api-design)
8. [Security Architecture](#security-architecture)
9. [Performance Considerations](#performance-considerations)
10. [Scalability](#scalability)
11. [Deployment Architecture](#deployment-architecture)

---

## System Overview

LaTeXZen is a web-based scientific paper converter and editor that enables:

- Document upload and processing
- Format conversion (PDF, DOCX, LaTeX, etc.)
- Template management (IEEE, MDPI, Springer)
- Real-time LaTeX editing
- Team collaboration
- Document sharing and versioning

### Core Capabilities

1. **Document Processing**: Extract text, images, tables, and math formulas from various document formats
2. **Format Conversion**: Convert documents between different scientific paper formats
3. **Template System**: Apply and customize templates for different publishers
4. **Collaboration**: Team-based document management with access control
5. **Version Control**: Track document changes and maintain history

---

## Architecture Patterns

### 1. Layered Architecture

```
┌─────────────────┐
│   Presentation  │  ← API Endpoints, JSON Responses
├─────────────────┤
│    Business     │  ← Services, Business Logic
│     Logic       │
├─────────────────┤
│     Data        │  ← Models, Database Access
│    Access       │
├─────────────────┤
│   Database      │  ← SQLite/PostgreSQL
└─────────────────┘
```

### 2. RESTful API Design

- **Resource-Oriented URLs**: `/teams`, `/templates`, `/documents`
- **HTTP Methods**: GET, POST, PATCH, DELETE
- **Stateless Authentication**: JWT tokens
- **JSON Data Format**: Consistent request/response structure

### 3. Microservices Readiness

- Modular service design
- Loose coupling between components
- Independent scalability potential
- Container-ready architecture

---

## Component Diagram

```
                                    ┌─────────────────────┐
                                    │      Nginx          │
                                    │  (Reverse Proxy)    │
                                    └──────────┬──────────┘
                                               │
                            ┌──────────────────┴──────────────────┐
                            │                                      │
                   ┌────────▼────────┐               ┌────────────▼────────┐
                   │   FastAPI App   │               │    Frontend         │
                   │   (Backend)     │               │  (React/Next.js)    │
                   └────────┬────────┘               │   (Future)          │
                            │                        └─────────────────────┘
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼───────┐   ┌───────────▼──────────┐
        │  Routers      │   │     Services          │
        │  - Teams      │   │  - Document Processing│
        │  - Templates  │   │  - Template Manager   │
        │  - Documents  │   │  - File Processing    │
        │  - Files      │   │  - LaTeX Compiler     │
        └───────┬───────┘   └───────────┬──────────┘
                │                       │
        ┌───────▼───────┐   ┌───────────▼──────────┐
        │   Models      │   │    Database           │
        │  - Users      │   │  - SQLite (dev)       │
        │  - Teams      │   │  - PostgreSQL (prod)  │
        │  - Templates  │   │                       │
        │  - Documents  │   └───────────────────────┘
        └───────────────┘
```

---

## Data Flow

### Document Upload Flow

```
User → File Upload → Validation → Storage → Processing → Database
                    ↓
            Virus Scan
            Format Check
            Size Validation
```

### Document Conversion Flow

```
Document → Parser → Structure Analysis → Template Application → Output Generation
             ↓
        ┌────────┴────────┐
        ↓                 ↓
    Text/Images      Math Formulas
        ↓                 ↓
    LaTeX Code       LaTeX Math
        └────────┬────────┘
                 ↓
           PDF Generation
```

### Authentication Flow

```
Login Request → Credentials Validation → JWT Token Generation → Response
                    ↓
            Database Query
                    ↓
            Password Verify
                    ↓
             Token Creation
```

---

## Technology Stack

### Backend Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | Web framework |
| Language | Python 3.11+ | Programming language |
| Database | SQLite/PostgreSQL | Data persistence |
| ORM | SQLAlchemy 2.0 | Database operations |
| Authentication | PyJWT + Bcrypt | Security |
| Validation | Pydantic | Data validation |

### Document Processing

| Component | Technology | Purpose |
|-----------|------------|---------|
| PDF Processing | PyMuPDF, pdfplumber | Extract text from PDFs |
| DOCX Processing | python-docx | Read Word documents |
| LaTeX | pdflatex | Compile LaTeX to PDF |
| OCR | Tesseract | Image text extraction |
| Images | Pillow, OpenCV | Image processing |

### Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| Containerization | Docker | Application packaging |
| Orchestration | Docker Compose | Container management |
| Web Server | Nginx | Reverse proxy |
| Process Manager | Systemd | Service management |

### Development Tools

| Component | Technology | Purpose |
|-----------|------------|---------|
| Code Formatting | Black, isort | Code style |
| Linting | Flake8 | Code quality |
| Testing | Pytest | Unit testing |
| Type Checking | Mypy | Type safety |

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255),
ESTAMP DEFAULT CURRENT    created_at TIM_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Teams Table
```sql
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Team Members Table
```sql
CREATE TABLE team_members (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id),
    user_id INTEGER REFERENCES users(id),
    role VARCHAR(50) NOT NULL,  -- owner, member, admin
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Templates Table
```sql
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- global, user, team
    content TEXT NOT NULL,
    visibility VARCHAR(50) NOT NULL,  -- public, private, team
    owner_id INTEGER REFERENCES users(id),
    team_id INTEGER REFERENCES teams(id),
    category_id INTEGER REFERENCES template_categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Documents Table
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    template_id INTEGER REFERENCES templates(id),
    owner_id INTEGER REFERENCES users(id),
    team_id INTEGER REFERENCES teams(id),
    visibility VARCHAR(50) NOT NULL,  -- personal, team, public
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Design

### RESTful Principles

1. **Resources**: Every endpoint represents a resource
2. **HTTP Methods**: GET (read), POST (create), PATCH (update), DELETE (remove)
3. **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found)
4. **Versioning**: URL-based versioning (`/api/v1/...`)

### API Endpoint Structure

```
Base URL: /api/v1

Authentication:
  POST   /register
  POST   /token
  GET    /users/me

Teams:
  POST   /teams
  GET    /teams
  GET    /teams/{id}
  POST   /teams/{id}/join
  POST   /teams/{id}/leave
  GET    /teams/{id}/members
  DELETE /teams/{id}/members/{user_id}

Templates:
  POST   /templates
  GET    /templates
  GET    /templates/{id}
  PATCH  /templates/{id}/visibility
  DELETE /templates/{id}
  GET    /template-categories
  POST   /template-categories

Documents:
  POST   /documents
  GET    /documents
  GET    /documents/{id}
  PATCH  /documents/{id}
  DELETE /documents/{id}
  POST   /documents/{id}/convert
  GET    /documents/{id}/export

Files:
  POST   /upload
  GET    /upload/{filename}
  DELETE /upload/{filename}
  POST   /upload/temp
  DELETE /temp/{filename}
```

---

## Security Architecture

### Authentication

- **JWT Tokens**: Stateless authentication
- **Token Expiration**: 30 minutes (configurable)
- **Password Hashing**: Bcrypt with salt
- **Secure Transport**: HTTPS required (in production)

### Authorization

- **Role-Based Access Control (RBAC)**
- **Resource-Level Permissions**
- **Visibility Controls**: public, private, team

### Data Protection

- **Input Validation**: P- **SQLydantic schemas
 Injection Prevention**: SQLAlchemy ORM
- **XSS Protection**: Output encoding
- **File Upload Security**: Format validation, size limits

### Security Headers

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance Considerations

### Database Optimization

- **Indexing**: Primary keys, foreign keys, frequently queried columns
- **Query Optimization**: Lazy loading, eager loading where appropriate
- **Connection Pooling**: SQLAlchemy connection pool

### Caching Strategy

- **Template Caching**: In-memory cache for frequently used templates
- **Query Result Caching**: Cache database query results
- **Static File Caching**: Nginx caching for static content

### Resource Management

- **File Upload Limits**: Maximum file size (10MB default)
- **Concurrent Request Limits**: Thread pool limits
- **Memory Management**: Efficient data structures, garbage collection

### Asynchronous Processing

- **Background Tasks**: For long-running operations
- **Non-blocking I/O**: FastAPI async support
- **Queue System**: For document processing jobs

---

## Scalability

### Horizontal Scaling

```
Load Balancer
     │
  ┌──┴──┐
  │     │
App   App   App  ← Stateless instances
  │     │
  └─────┘
     │
 Database
```

### Vertical Scaling

- Increase CPU cores for processing
- Increase RAM for larger documents
- Use SSD storage for faster I/O

### Microservices Potential

- Separate document processing service
- Independent template service
- Dedicated authentication service

---

## Deployment Architecture

### Development Environment

```
Local Machine
├─ FastAPI App (uvicorn)
├─ SQLite Database
└─ File Storage (local)
```

### Production Environment (Docker)

```
VPS/Server
├─ Docker Container 1: App
├─ Docker Container 2: Nginx
└─ Volume Storage
   ├─ Documents
   ├─ Processed
   └─ Logs
```

### Production Environment (Kubernetes)

```
Kubernetes Cluster
├─ Deployment: App
├─ Service: App
├─ Ingress: Nginx
├─ PersistentVolume: Database
└─ PersistentVolume: Files
```

---

## Future Architecture Enhancements

1. **Microservices Architecture**
   - Separate services for document processing, templates, users
   - Independent scaling based on load

2. **Message Queue**
   - RabbitMQ or Kafka for async processing
   - Better handling of long-running tasks

3. **Caching Layer**
   - Redis for session management
   - Template caching
   - Query result caching

4. **CDN Integration**
   - Static file delivery
   - Geographic distribution

5. **Multi-Region Deployment**
   - Geographic redundancy
   - Reduced latency

---

## Monitoring and Logging

### Application Metrics

- Request/response times
- Error rates
- Active users
- Document processing stats

### Logging Strategy

- **Application Logs**: Python logging module
- **Access Logs**: Nginx access logs
- **Error Logs**: Separate error log files
- **Audit Logs**: User actions, system events

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Conclusion

The LaTeXZen architecture is designed to be:

- **Modular**: Easy to maintain and extend
- **Scalable**: Can grow with user base
- **Secure**: Built with security in mind
- **Performant**: Optimized for speed
- **Reliable**: Robust error handling and recovery

This architecture provides a solid foundation for current functionality while allowing for future enhancements and scaling.

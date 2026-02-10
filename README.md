# LaTeXZen - Scientific Paper Converter

A comprehensive web application for converting documents to scientific paper formats (IEEE, MDPI, Springer, etc.) with integrated LaTeX editor functionality.

##  Features

### Core Functionality
- **Document Upload & Processing**: Support for PDF, DOCX, TXT, LaTeX, and image formats
- **Structure Analysis**: Extract and understand document structure including text, images, graphs, and math formulas
- **Format Conversion**: Convert documents to various scientific paper formats
- **Web-Based LaTeX Editor**: Full-featured LaTeX editor with real-time preview (coming soon)

### Template System
- **Standard Templates**: IEEE, MDPI, Springer templates included
- **Custom Templates**: Create and share templates according to publisher guidelines
- **Template Categories**: Organize templates by journal, conference, or purpose
- **Template Validation**: Ensure templates meet publisher requirements

### Collaboration
- **Team Management**: Create teams, invite members, manage roles
- **Document Sharing**: Share documents within teams or publicly
- **Template Sharing**: Share templates globally or within teams
- **Access Control**: Granular permissions for documents and templates

### Document Management
- **Version Control**: Track document versions and changes
- **Citation Management**: Manage citations and references
- **Export Options**: Export to LaTeX, PDF, and other formats

##  Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- LaTeX distribution (for PDF compilation)

### Installation

#### 1. Clone the Repository
```bash
git clone git@github.com:lef-zach/la-texzen.git
cd la-texzen
```

#### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
. venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install LaTeX Distribution

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    poppler-utils \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    lmodern \
    cm-super
```

**Windows:**
- Download and install MiKTeX: https://miktex.org/download
- Or install TeX Live: https://www.tug.org/texlive/

**macOS:**
```bash
brew install --cask mactex
```

#### 5. Run the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 6. Access the Application
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Interactive API**: http://localhost:8000/docs

## 📖 Documentation

### User Documentation
- [User Guide](docs/USER_GUIDE.md) - Complete user manual
- [Template Guide](docs/TEMPLATE_GUIDE.md) - How to use and create templates
- [API Reference](docs/API.md) - Complete API documentation

### Developer Documentation
- [Architecture Overview](docs/ARCHITECTURE.md) - System architecture
- [Development Guide](docs/DEVELOPMENT.md) - Setting up development environment
- [Contribution Guide](docs/CONTRIBUTING.md) - How to contribute

### Deployment Documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Docker Guide](docs/DOCKER.md) - Docker configuration
- [Security Guide](docs/SECURITY.md) - Security best practices

##  API Endpoints

### Authentication
```http
POST /register          # Register new user
POST /token            # Login and get access token
GET  /users/me         # Get current user info
```

### Teams
```http
POST   /teams                    # Create new team
GET    /teams                   # Get user's teams
GET    /teams/{team_id}         # Get team details
POST   /teams/{team_id}/join    # Join team
POST   /teams/{team_id}/leave   # Leave team
GET    /teams/{team_id}/members # Get team members
DELETE /teams/{team_id}/members/{user_id}  # Remove member
```

### Templates
```http
POST   /templates                    # Create template
GET    /templates                   # Get available templates
GET    /templates/{template_id}     # Get template details
PATCH  /templates/{template_id}/visibility  # Update visibility
DELETE /templates/{template_id}     # Delete template
GET    /template-categories         # Get template categories
POST   /template-categories         # Create category
```

### Documents
```http
POST   /documents                    # Create document
GET    /documents                   # Get user's documents
GET    /documents/{document_id}     # Get document details
PATCH  /documents/{document_id}     # Update document
DELETE /documents/{document_id}     # Delete document
POST   /documents/{document_id}/convert    # Convert format
GET    /documents/{document_id}/export     # Export document
```

### Files
```http
POST /upload           # Upload file
GET /upload/{filename} # Get uploaded file
DELETE /upload/{filename}  # Delete uploaded file
POST /upload/temp      # Upload temporary file
DELETE /temp/{filename}  # Delete temporary file
```

##  Architecture

```
la-texzen/
├── app/
│   ├── __init__.py              # App initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── database.py              # Database configuration
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── hashing.py               # Password hashing utilities
│   ├── dependencies.py          # Dependency injection
│   ├── routers/                 # API route handlers
│   │   ├── teams.py             # Team endpoints
│   │   ├── templates.py         # Template endpoints
│   │   ├── documents.py         # Document endpoints
│   │   └── files.py             # File upload endpoints
│   ├── services/                # Business logic
│   │   ├── document_processing.py  # Document processing
│   │   └── template_manager.py     # Template management
│   └── utils/                   # Utility functions
├── templates/                   # LaTeX templates
│   ├── ieee/
│   ├── mdpi/
│   └── springer/
├── documents/                   # Uploaded documents
├── processed/                   # Processed documents
├── logs/                        # Application logs
├── backups/                     # Database backups
├── tmp/                         # Temporary files
├── docs/                        # Documentation
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

##  Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with PyJWT
- **Password Hashing**: Bcrypt with Passlib

### Document Processing
- **PDF Processing**: PyMuPDF, pdfplumber
- **DOCX Processing**: python-docx
- **OCR**: Tesseract, OpenCV
- **LaTeX Compilation**: pdflatex
- **Image Processing**: Pillow, OpenCV

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx
- **Process Manager**: Systemd

### Development Tools
- **Code Formatting**: Black, isort
- **Linting**: Flake8
- **Testing**: Pytest
- **Type Checking**: Mypy

##  Installation with Docker

### Quick Start with Docker

```bash
# Clone and enter directory
git clone git@github.com:lef-zach/la-texzen.git
cd la-texzen

# Build and start containers
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop containers
docker-compose down
```

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Docker Services

1. **app** - Main FastAPI application
2. **nginx** - Reverse proxy and load balancer

##  Security

- All passwords are hashed using bcrypt
- JWT tokens for authentication
- File upload validation and limits
- CORS configuration
- Input validation and sanitization

##  Performance

- Database indexing for fast queries
- Caching for templates
- Asynchronous processing for document conversion
- Resource limits in Docker deployment
- Connection pooling for database

##  Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_auth.py
```

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Contributing

Contributions are welcome! Please read our [Contributing Guide](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

##  Support

For support, please open an issue on GitHub or contact the maintainers.

##  Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit
- [LaTeX Project](https://www.latex-project.org/) - Document preparation system
- [Docker](https://www.docker.com/) - Containerization platform

---



For the latest updates, please visit our [GitHub Repository](https://github.com/lef-zach/la-texzen).

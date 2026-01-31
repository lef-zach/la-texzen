# Scientific Paper Converter

A web application for converting documents to scientific paper formats (IEEE, MDPI, Springer, etc.) with LaTeX editor functionality.

## Features

- **Document Upload**: Support for PDF, DOCX, TXT, LaTeX, and image formats
- **Document Processing**: Extract and understand document structure including text, images, graphs, and math formulas
- **Format Conversion**: Convert documents to various scientific paper formats
- **LaTeX Editor**: Web-based LaTeX editor with real-time preview
- **Template Management**: IEEE, MDPI, Springer templates with custom template creation
- **Team Collaboration**: Create teams, share templates and documents
- **Citation Management**: Manage citations and references
- **Version Control**: Track document versions and changes

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (default), PostgreSQL (production)
- **Frontend**: React + Next.js (planned)
- **Document Processing**: Custom Python services
- **LaTeX Compilation**: pdflatex
- **Containerization**: Docker
- **Deployment**: Docker Compose

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- LaTeX distribution (for PDF compilation)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd paper-converter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
. venv/Scripts/activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install LaTeX distribution:
   - **Linux**: `sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra`
   - **Windows**: Install MiKTeX or TeX Live
   - **Mac**: Install MacTeX

### Running the Application

1. Start the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
   - API documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running with Docker

```bash
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user information

### Teams
- `POST /teams` - Create a new team
- `GET /teams` - Get user's teams
- `GET /teams/{team_id}` - Get team details
- `POST /teams/{team_id}/join` - Join a team
- `POST /teams/{team_id}/leave` - Leave a team
- `GET /teams/{team_id}/members` - Get team members
- `DELETE /teams/{team_id}/members/{user_id}` - Remove team member

### Templates
- `POST /templates` - Create a new template
- `GET /templates` - Get available templates
- `GET /templates/{template_id}` - Get template details
- `PATCH /templates/{template_id}/visibility` - Update template visibility
- `DELETE /templates/{template_id}` - Delete a template
- `GET /template-categories` - Get template categories
- `POST /template-categories` - Create a template category

### Documents
- `POST /documents` - Create a new document
- `GET /documents` - Get user's documents
- `GET /documents/{document_id}` - Get document details
- `PATCH /documents/{document_id}` - Update a document
- `DELETE /documents/{document_id}` - Delete a document
- `POST /documents/{document_id}/convert` - Convert document to different format
- `GET /documents/{document_id}/export` - Export document in different formats

### Files
- `POST /upload` - Upload a file
- `GET /upload/{filename}` - Get uploaded file
- `DELETE /upload/{filename}` - Delete uploaded file
- `POST /upload/temp` - Upload temporary file
- `DELETE /temp/{filename}` - Delete temporary file

## Project Structure

```
paper-converter/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── hashing.py              # Password hashing
│   ├── dependencies.py         # Dependency injection
│   ├── routers/                # API routes
│   │   ├── __init__.py
│   │   ├── teams.py           # Team endpoints
│   │   ├── templates.py       # Template endpoints
│   │   ├── documents.py       # Document endpoints
│   │   └── files.py           # File upload endpoints
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── document_processing.py
│   │   └── template_manager.py
│   └── utils/                 # Utilities
│       └── __init__.py
├── templates/                 # LaTeX templates
│   ├── ieee/
│   ├── mdpi/
│   └── springer/
├── documents/                 # Uploaded documents
├── processed/                 # Processed documents
├── logs/                      # Application logs
├── backups/                   # Database backups
├── tmp/                       # Temporary files
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection URL (default: `sqlite:///./app.db`)
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: `30`)

### Template Customization

Templates are stored in the `templates/` directory. You can create custom templates for any publisher by following the existing template structure.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
black app/
isort app/
flake8 app/
```

## Deployment

### Docker Deployment

1. Build the Docker image:
```bash
docker-compose build
```

2. Start the services:
```bash
docker-compose up -d
```

3. Check logs:
```bash
docker-compose logs -f
```

### Manual Deployment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create systemd service:
```bash
sudo nano /etc/systemd/system/paper-converter.service
```

3. Enable and start service:
```bash
sudo systemctl enable paper-converter
sudo systemctl start paper-converter
```

## Security Considerations

- All passwords are hashed using bcrypt
- JWT tokens for authentication
- File upload validation
- CORS configuration
- Rate limiting (to be implemented)

## Performance Considerations

- Database indexing for fast queries
- Caching for templates
- Asynchronous processing for document conversion
- Resource limits in Docker deployment

## Future Enhancements

- Frontend with React + Next.js
- Real-time collaboration
- Advanced OCR for scanned documents
- Math formula recognition
- Table extraction
- Citation management integration
- Export to multiple formats (Word, HTML, etc.)
- Mobile application

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
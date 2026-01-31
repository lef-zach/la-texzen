# Setup Guide

Complete setup guide for LaTeXZen Scientific Paper Converter.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Manual Installation](#manual-installation)
4. [Docker Installation](#docker-installation)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 22.04 LTS (or equivalent)

### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 50GB SSD
- **OS**: Ubuntu 22.04 LTS (or equivalent)

### Required Software
- Python 3.11+
- Git
- LaTeX distribution
- Docker & Docker Compose (optional)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone git@github.com:lef-zach/la-texzen.git
cd la-texzen
```

### 2. Run with Docker (Recommended)

```bash
# Build and start containers
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Access the application
# API Docs: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### 3. Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
. venv/Scripts/activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Install LaTeX
# Linux: sudo apt-get install texlive-latex-base
# Windows: Install MiKTeX or TeX Live
# Mac: Install MacTeX

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Manual Installation

### Step 1: Install Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**Windows:**
1. Download Python 3.11 from https://python.org/downloads/
2. Run the installer
3. Check "Add Python to PATH"

**macOS:**
```bash
brew install python@3.11
```

### Step 2: Install Git

**Ubuntu/Debian:**
```bash
sudo apt install git
```

**Windows/macOS:**
Download from https://git-scm.com/downloads

### Step 3: Clone Repository

```bash
git clone git@github.com:lef-zach/la-texzen.git
cd la-texzen
```

### Step 4: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows:
. venv\Scripts\activate

# Verify activation
python --version
```

### Step 5: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 6: Install LaTeX Distribution

**Ubuntu/Debian:**
```bash
sudo apt update
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
1. Download MiKTeX: https://miktex.org/download
2. Run the installer
3. Follow the setup wizard
4. Ensure pdflatex is in PATH

**macOS:**
```bash
# Using Homebrew
brew install --cask mactex

# Or download from https://www.tug.org/mactex/
```

### Step 7: Configure Environment

Create a `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 8: Initialize Database

```bash
# Create database tables
python -c "from app.database import create_tables; create_tables()"
```

### Step 9: Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 10: Verify Installation

```bash
# Test API endpoints
curl http://localhost:8000/

# Expected response:
# {"message":"Scientific Paper Converter API"}
```

---

## Docker Installation

### Step 1: Install Docker

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

**Windows/macOS:**
Download Docker Desktop from https://www.docker.com/products/docker-desktop

### Step 2: Install Docker Compose

```bash
# Ubuntu/Debian
sudo apt install docker-compose

# Or using pip
pip install docker-compose
```

### Step 3: Verify Docker Installation

```bash
docker --version
docker-compose --version
```

### Step 4: Clone and Build

```bash
git clone git@github.com:lef-zach/la-texzen.git
cd la-texzen

# Build the image
docker-compose build

# Start the containers
docker-compose up -d

# View logs
docker-compose logs -f app
```

### Step 5: Access the Application

```bash
# API Documentation
http://localhost:8000/docs

# ReDoc Documentation
http://localhost:8000/redoc
```

---

## Verification

### 1. Check Running Services

```bash
# Docker
docker-compose ps

# Should show:
#   Name                 Command               State           Ports
# ----------------------------------------------------------------------
# app         uvicorn app.main:app --host ...   Up              0.0.0.0:80->80/tcp
# nginx       nginx -g daemon off;              Up              0.0.0.0:80->80/tcp
```

### 2. Test API Endpoints

```bash
# Test root endpoint
curl http://localhost:8000/
# Expected: {"message":"Scientific Paper Converter API"}

# Test registration
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User","password":"test123"}'
```

### 3. Check Logs

```bash
# Docker logs
docker-compose logs -f app

# Application should start without errors
```

---

## Troubleshooting

### Python Version Issues

**Problem:** Python version too old
```bash
# Check version
python --version

# If < 3.11, install newer version
# Ubuntu/Debian:
sudo apt install python3.11
```

### Virtual Environment Issues

**Problem:** Virtual environment not activating
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dependency Installation Issues

**Problem:** pip install fails
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies separately
pip install fastapi uvicorn sqlalchemy

# Clear pip cache
pip cache purge
```

### Database Issues

**Problem:** Database connection errors
```bash
# Check database file exists
ls -la app.db

# Recreate database
rm app.db
python -c "from app.database import create_tables; create_tables()"
```

### LaTeX Issues

**Problem:** PDF compilation fails
```bash
# Check LaTeX installation
pdflatex --version

# Reinstall LaTeX
# Ubuntu/Debian:
sudo apt-get install --reinstall texlive-latex-base

# Check log files
ls -la logs/
```

### Port Already in Use

**Problem:** Port 8000 already in use
```bash
# Find process using port
netstat -tulpn | grep :8000

# Kill the process
sudo kill <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Docker Issues

**Problem:** Container fails to start
```bash
# View container logs
docker-compose logs app

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Permission Issues

**Problem:** Permission denied errors
```bash
# Fix permissions
chmod +x venv/bin/activate
sudo chown -R $USER:$USER .

# For Docker
sudo usermod -aG docker $USER
newgrp docker
```

### Memory Issues

**Problem:** Out of memory errors
```bash
# Check memory usage
free -m

# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Next Steps

1. **Read the API Documentation**: http://localhost:8000/docs
2. **Set up your first team**: See User Guide
3. **Create your first document**: See User Guide
4. **Explore templates**: See Template Guide

---

## Getting Help

If you encounter issues not covered here:

1. Check the [FAQ](docs/FAQ.md)
2. Search existing [GitHub Issues](https://github.com/lef-zach/la-texzen/issues)
3. Open a new issue with:
   - Operating system and version
   - Python version
   - Complete error message
   - Steps to reproduce the issue

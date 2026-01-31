# Deployment Guide

Complete deployment guide for LaTeXZen Scientific Paper Converter.

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Docker Deployment](#docker-deployment)
3. [Manual Deployment](#manual-deployment)
4. [VPS Deployment](#vps-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [SSL Configuration](#ssl-configuration)
7. [Monitoring](#monitoring)
8. [Backup and Recovery](#backup-and-recovery)
9. [Troubleshooting](#troubleshooting)

---

## Deployment Options

### Option 1: Docker (Recommended)
- Quick setup
- Consistent environment
- Easy scaling
- Isolated dependencies

### Option 2: Manual Deployment
- Full control
- Lower resource overhead
- More complex setup
- Requires manual updates

### Option 3: Cloud Services
- Managed infrastructure
- Automatic scaling
- Higher cost
- Vendor lock-in

---

## Docker Deployment

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB RAM available
- 10GB disk space

### Quick Start

```bash
# 1. Clone repository
git clone git@github.com:lef-zach/la-texzen.git
cd la-texzen

# 2. Create environment file
cp .env.example .env
# Edit .env with your configuration

# 3. Build and start containers
docker-compose up -d --build

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f app
```

### Docker Configuration

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    poppler-utils \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    lmodern \
    cm-super \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p documents processed logs backups tmp templates

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "80:80"
      - "443:443"
    environment:
      - DATABASE_URL=sqlite:///./app.db
      - SECRET_KEY=your-secret-key-here
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    volumes:
      - ./documents:/app/documents
      - ./processed:/app/processed
      - ./logs:/app/logs
      - ./backups:/app/backups
      - ./tmp:/app/tmp
      - ./templates:/app/templates
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    restart: unless-stopped

volumes:
  documents:
  processed:
  logs:
  backups:
  tmp:
  templates:
```

### Docker Management Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f app

# Rebuild containers
docker-compose up -d --build

# View running containers
docker-compose ps

# Check container resource usage
docker stats

# Clean up unused resources
docker system prune -a
```

---

## Manual Deployment

### Server Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB SSD
- OS: Ubuntu 22.04 LTS

**Recommended:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB SSD
- OS: Ubuntu 22.04 LTS

### Step 1: Server Setup

```bash
# Connect to server
ssh user@your-server-ip

# Update system
sudo apt update
sudo apt upgrade -y

# Create user
sudo adduser latexzen
sudo usermod -aG sudo latexzen

# Switch to user
sudo su - latexzen
```

### Step 2: Install Dependencies

```bash
# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install Git
sudo apt install git

# Install LaTeX
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

### Step 3: Deploy Application

```bash
# Clone repository
git clone git@github.com:lef-zach/la-texzen.git
cd la-texzen

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# Create directories
mkdir -p documents processed logs backups tmp templates

# Initialize database
python -c "from app.database import create_tables; create_tables()"
```

### Step 4: Configure Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/latexzen.service
```

```ini
[Unit]
Description=LaTeXZen Scientific Paper Converter
After=network.target

[Service]
User=latexzen
Group=latexzen
WorkingDirectory=/home/latexzen/la-texzen
Environment="PATH=/home/latexzen/la-texzen/venv/bin"
Environment="DATABASE_URL=sqlite:///./app.db"
Environment="SECRET_KEY=your-super-secret-key"
ExecStart=/home/latexzen/la-texzen/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable latexzen
sudo systemctl start latexzen

# Check status
sudo systemctl status latexzen

# View logs
sudo journalctl -u latexzen -f
```

### Step 5: Configure Nginx

```bash
# Install Nginx
sudo apt install nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/latexzen
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/latexzen/la-texzen/static;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/latexzen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## VPS Deployment

### Recommended VPS Providers

1. **DigitalOcean**
   - Droplets: $20-40/month
   - Easy setup
   - Good documentation

2. **Vultr**
   - Instances: $15-30/month
   - High performance
   - Global locations

3. **Hetzner**
   - VPS: €6-15/month
   - Excellent value
   - EU-based

4. **Linode**
   - Linodes: $20-40/month
   - Reliable service
   - Good support

### Proxmox VM Setup

```bash
# Create VM
# 1. Download Ubuntu 22.04 ISO
# 2. Create new VM in Proxmox
# 3. Attach ISO and install Ubuntu
# 4. Configure network
# 5. Follow manual deployment steps above
```

### Security Hardening

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Configure firewall
sudo ufw allow OpenSSH
sudo ufw allow http
sudo ufw allow https
sudo ufw enable

# Setup automatic updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## Cloud Deployment

### AWS EC2

```bash
# Launch EC2 instance
# 1. Choose Ubuntu Server 22.04 LTS
# 2. Select instance type (t3.medium recommended)
# 3. Configure security group (ports 22, 80, 443)
# 4. Connect via SSH
# 5. Follow manual deployment steps
```

### Google Cloud Platform

```bash
# Create VM instance
# 1. Go to Compute Engine
# 2. Create instance
# 3. Choose Ubuntu 22.04 LTS
# 4. Configure firewall rules
# 5. Connect via SSH
# 6. Follow manual deployment steps
```

### Azure

```bash
# Create Virtual Machine
# 1. Go to Virtual Machines
# 2. Create new VM
# 3. Choose Ubuntu Server 22.04
# 4. Configure network security group
# 5. Connect via SSH
# 6. Follow manual deployment steps
```

---

## SSL Configuration

### Using Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Manual SSL Setup

```bash
# Generate self-signed certificate (testing only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/server.key \
  -out /etc/nginx/ssl/server.crt

# Update Nginx configuration
sudo nano /etc/nginx/sites-available/latexzen
```

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}
```

---

## Monitoring

### Application Monitoring

```bash
# Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash

# Check if service is running
if systemctl is-active --quiet latexzen; then
    echo "Service is running"
    exit 0
else
    echo "Service is not running"
    exit 1
fi
EOF

chmod +x monitor.sh

# Add to cron for monitoring
crontab -e
# Add: */5 * * * * /home/latexzen/la-texzen/monitor.sh
```

### Log Management

```bash
# Configure log rotation
sudo nano /etc/logrotate.d/latexzen
```

```
/home/latexzen/la-texzen/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 644 latexzen latexzen
    postrotate
        systemctl restart latexzen > /dev/null 2>&1 || true
    endscript
}
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected"
    }
```

---

## Backup and Recovery

### Automated Backups

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/home/latexzen/la-texzen/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
cp /home/latexzen/la-texzen/app.db "$BACKUP_DIR/app_$DATE.db"

# Keep only last 7 backups
ls -t "$BACKUP_DIR"/app_*.db | tail -n +8 | xargs rm -f

echo "Backup completed: app_$DATE.db"
EOF

chmod +x backup.sh

# Add to cron
crontab -e
# Add: 0 2 * * * /home/latexzen/la-texzen/backup.sh
```

### Recovery Procedure

```bash
# Stop service
sudo systemctl stop latexzen

# Restore from backup
cp /home/latexzen/la-texzen/backups/app_20240101_020000.db /home/latexzen/la-texzen/app.db

# Start service
sudo systemctl start latexzen
```

### Offsite Backup

```bash
# Sync to S3
aws s3 sync /home/latexzen/la-texzen/backups s://your-backup-bucket/

# Or use rclone
rclone sync /home/latexzen/la-textexzen/backups remote:backup
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status latexzen

# View logs
sudo journalctl -u latexzen -n 100

# Check port usage
netstat -tulpn | grep :8000

# Test configuration
python -c "from app.main import app; print('Config OK')"
```

### Database Issues

```bash
# Check database file
ls -la app.db

# Test database connection
python -c "from app.database import engine; engine.connect()"

# Recreate database
rm app.db
python -c "from app.database import create_tables; create_tables()"
```

### Performance Issues

```bash
# Check memory usage
free -m

# Check CPU usage
top

# Check disk usage
df -h

# Check database size
du -sh app.db
```

### Network Issues

```bash
# Test connectivity
curl http://localhost:8000/

# Check firewall
sudo ufw status

# Test DNS resolution
nslookup your-domain.com
```

---

## Next Steps

1. **Set up monitoring**: Configure alerting
2. **Implement backups**: Automated daily backups
3. **Configure SSL**: Let's Encrypt certificate
4. **Set up logging**: Centralized log management
5. **Configure CDN**: For static files

---

## Support

For deployment issues:
1. Check the [FAQ](docs/FAQ.md)
2. Search [GitHub Issues](https://github.com/lef-zach/la-texzen/issues)
3. Open a new issue with deployment details

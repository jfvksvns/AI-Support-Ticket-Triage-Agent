# Setup & Deployment Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Database Setup](#database-setup)
5. [Sample Data](#sample-data)
6. [Running Tests](#running-tests)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## Prerequisites

### Required
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- Claude API key from [Anthropic Console](https://console.anthropic.com/account/keys)

### Optional
- Docker & Docker Compose (for containerized deployment)
- Git (for version control)
- PostgreSQL (for production database upgrade)

---

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd ai-support-ticket-triage
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env
# Required: Set CLAUDE_API_KEY=sk-ant-your-key-here
```

### Step 3: Initialize Database

```bash
# From backend directory
python scripts/init_db.py
```

Expected output:
```
✓ Database initialized successfully!
```

### Step 4: Start Backend Server

```bash
# From backend directory
python main.py
```

Backend will start at `http://localhost:8000`

**Verify:**
- API Health: `curl http://localhost:8000/api/health`
- Swagger Docs: Visit `http://localhost:8000/api/docs`

### Step 5: Frontend Setup

In a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Frontend will start at `http://localhost:5173`

### Step 6: Generate Sample Data (Optional)

```bash
cd backend
python scripts/generate_sample_data.py
```

This creates 30 diverse sample tickets for testing.

---

## Docker Deployment

### Prerequisites
- Docker installed and running
- Docker Compose installed
- Claude API key

### Step 1: Set Environment Variables

```bash
# Set your Claude API key
export CLAUDE_API_KEY="sk-ant-your-key-here"

# Optional: Set other variables
export DATABASE_URL="sqlite:///./tickets.db"
export LOG_LEVEL="INFO"
```

### Step 2: Build Images

```bash
# Build all images
docker-compose build

# Or build specific services
docker-compose build backend
docker-compose build frontend
```

### Step 3: Start Services

```bash
# Start all services in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Step 4: Verify Services

```bash
# Check service status
docker-compose ps

# Test backend health
curl http://localhost:8000/api/health

# Test frontend
open http://localhost:3000  # macOS
# or
xdg-open http://localhost:3000  # Linux
# or
start http://localhost:3000  # Windows
```

### Step 5: Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop backend
docker-compose stop frontend
```

---

## Database Setup

### SQLite (Development/Testing)

```bash
# Already configured in .env
DATABASE_URL=sqlite:///./tickets.db

# Initialize
python backend/scripts/init_db.py

# Database file location
ls -lh backend/tickets.db
```

### PostgreSQL (Production)

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE ticket_triage;
CREATE USER ticket_user WITH PASSWORD 'your-secure-password';
ALTER ROLE ticket_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE ticket_triage TO ticket_user;
```

3. Update .env:
```bash
DATABASE_URL=postgresql://ticket_user:password@localhost:5432/ticket_triage
```

4. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

5. Initialize:
```bash
python backend/scripts/init_db.py
```

---

## Sample Data

### Generate Sample Tickets

```bash
cd backend
python scripts/generate_sample_data.py
```

**Output:**
```
Initializing database...
✓ Database initialized
✓ Cleared existing tickets
✓ Created 30 sample tickets

📊 Sample Data Summary:
   Total tickets: 30
   Categories: 10
   Statuses: 6
   Urgencies: 4
   Avg confidence: 85.2%
   For review: 4

✅ Sample data generation completed successfully!
```

**Includes:**
- 30 diverse tickets across all categories
- Various urgency levels
- Mixed statuses
- Different departments
- Realistic descriptions
- AI classifications with reasoning

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::TestClassifyEndpoint::test_classify_valid_ticket -v

# Run with output
pytest tests/ -v -s
```

**Expected Results:**
- 80+ tests passing
- Coverage > 80%
- All endpoints tested
- All services tested
- Database operations tested

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test -- --coverage
```

### Integration Testing

1. Start both services
2. Create a test ticket via form
3. Verify it appears in list
4. Check statistics update
5. Update ticket status
6. Delete ticket
7. Verify classification accuracy

---

## Troubleshooting

### Backend Issues

**ModuleNotFoundError**
```bash
# Ensure virtual environment is active
source venv/bin/activate
pip install -r requirements.txt
```

**Database Error: "no such table: tickets"**
```bash
python backend/scripts/init_db.py
```

**Claude API Error: "Invalid API Key"**
```bash
# Verify .env file
cat backend/.env | grep CLAUDE_API_KEY

# Update with correct key
nano backend/.env
```

**Port 8000 already in use**
```bash
# Change port in .env
PORT=8001
```

**Database locked (SQLite)**
```bash
# Remove lock files
rm backend/*.db-journal
# Restart server
```

### Frontend Issues

**Port 5173 already in use**
```bash
npm run dev -- --port 3001
```

**API connection refused**
```bash
# Ensure backend is running
curl http://localhost:8000/api/health

# Check VITE_API_URL in .env
cat frontend/.env | grep VITE_API_URL
```

**Node modules issue**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Build errors**
```bash
# Clear build cache
rm -rf dist
npm run build
```

### Docker Issues

**Container won't start**
```bash
# Check logs
docker-compose logs -f

# Rebuild without cache
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Permission denied**
```bash
# Ensure Docker daemon is running
docker ps

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
```

**Port conflicts**
```bash
# Map to different ports
# Edit docker-compose.yml
ports:
  - "8001:8000"  # backend
  - "3001:3000"  # frontend
```

---

## Production Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group with ports 80, 443 open

2. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

3. **Clone Repository**
```bash
git clone <repo-url>
cd ai-support-ticket-triage
```

4. **Setup Environment**
```bash
sudo nano .env
# Set CLAUDE_API_KEY and other production settings
```

5. **Start Services**
```bash
docker-compose up -d
```

6. **Setup Reverse Proxy (Nginx)**
```bash
sudo apt-get install nginx

sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host \$host;
    }

    location /api/ {
        proxy_pass http://backend/api/;
        proxy_set_header Host \$host;
    }
}
EOF

sudo systemctl restart nginx
```

7. **Setup SSL with Let's Encrypt**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Heroku Deployment

1. **Prepare for Heroku**
```bash
echo "web: gunicorn app.main:app" > Procfile
pip install gunicorn
```

2. **Deploy**
```bash
heroku create your-app-name
heroku config:set CLAUDE_API_KEY=your-key
git push heroku main
```

### Performance Optimization

1. **Database**
   - Use PostgreSQL instead of SQLite
   - Add database backups
   - Enable query caching

2. **Caching**
   - Add Redis for response caching
   - Cache statistics (1-5 minute TTL)
   - Cache API responses

3. **Scaling**
   - Use load balancer
   - Horizontal scaling (multiple backend instances)
   - Database read replicas

---

## Monitoring & Maintenance

### Logs

```bash
# Backend logs
docker-compose logs -f backend --tail 100

# Frontend logs
docker-compose logs -f frontend --tail 100

# Check specific error
docker-compose logs backend | grep ERROR
```

### Performance

```bash
# Monitor resource usage
docker stats

# Check database size
du -h backend/tickets.db

# Analyze slow queries (PostgreSQL)
EXPLAIN ANALYZE SELECT * FROM tickets WHERE urgency = 'Critical';
```

### Backups

```bash
# Backup database
cp backend/tickets.db backend/tickets.db.backup

# Backup with timestamp
cp backend/tickets.db backend/tickets.db.backup.$(date +%Y%m%d)

# Restore from backup
cp backend/tickets.db.backup backend/tickets.db
```

---

## Support

For issues, refer to:
- Main README.md
- Troubleshooting section above
- GitHub Issues
- API Documentation at `/api/docs`

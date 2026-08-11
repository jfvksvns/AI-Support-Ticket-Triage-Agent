# 🤖 AI Support Ticket Triage Agent

An intelligent, production-ready AI-powered support ticket classification and routing system built with React, FastAPI, Claude AI, and SQLite.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Node 18+](https://img.shields.io/badge/Node-18%2B-green)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)

## 🎯 Overview

The AI Support Ticket Triage Agent automatically classifies incoming IT support tickets using Claude AI, assigns urgency levels, routes them to appropriate teams, and provides suggested responses. The system features a modern React dashboard with real-time statistics, comprehensive filtering, and complete ticket lifecycle management.

### Key Features

✨ **Intelligent Classification**
- AI-powered ticket analysis using Claude
- Automatic category assignment (10 categories)
- Urgency level assessment (Low → Critical)
- Confidence scoring (0-100%)
- Human review flagging for ambiguous cases

📊 **Professional Dashboard**
- Real-time statistics and metrics
- Interactive charts (pie, bar, distribution)
- Ticket trends over time
- Team workload visualization
- Dark mode support

🎫 **Complete Ticket Management**
- Create tickets with detailed forms
- View all tickets with advanced filtering
- Search by subject or description
- Sort by urgency, category, status
- Pagination (10-50 items per page)
- Quick status updates
- Delete tickets with confirmation

🔗 **Team Routing**
- Automatic assignment to appropriate teams:
  - IT Support
  - Network Team
  - Security Team
  - Cloud Team
  - Database Team
  - Application Team
  - Service Desk

⚡ **Production Features**
- Comprehensive error handling
- Input validation & sanitization
- RESTful API with Swagger documentation
- Type-safe TypeScript throughout
- 80+ unit tests
- Docker & Docker Compose ready

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  React Frontend (3000)                   │
│         TypeScript • Vite • TailwindCSS • Recharts      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend (8000)                  │
│     Python • SQLAlchemy • Pydantic • Uvicorn           │
└────────────────────────┬────────────────────────────────┘
                         │ SQL
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  SQLite Database                        │
│         Ticket Storage • AI Classifications            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼ HTTP/API
┌─────────────────────────────────────────────────────────┐
│                  Claude AI (Anthropic)                  │
│         Classification • Routing • Suggestions          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Claude API key from [Anthropic Console](https://console.anthropic.com/account/keys)
- Docker & Docker Compose (optional, for containerized deployment)

### Option 1: Local Development (Recommended for Development)

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-ticket-triage.git
cd ai-ticket-triage
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY

# Run server
python main.py
```

Backend will be available at: `http://localhost:8000`
- API: `http://localhost:8000/api`
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

#### 3. Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### Option 2: Docker Deployment (Recommended for Production)

```bash
# Set environment variable
export CLAUDE_API_KEY="sk-ant-your-key-here"

# Start the entire stack
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the stack
docker-compose down
```

Services will be available at:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/docs`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication
Optional API key via header:
```
X-API-Key: your-api-key-here
```

### Core Endpoints

#### Classification
- **POST** `/classify` - Classify ticket without saving
  ```bash
  curl -X POST http://localhost:8000/api/classify \
    -H "Content-Type: application/json" \
    -d '{
      "subject": "Cannot connect to VPN",
      "description": "I've been unable to connect..."
    }'
  ```

#### Tickets
- **POST** `/tickets` - Create new ticket (with auto-classification)
- **GET** `/tickets` - List tickets with filtering & pagination
- **GET** `/tickets/{id}` - Get ticket details
- **PATCH** `/tickets/{id}/status` - Update ticket status
- **DELETE** `/tickets/{id}` - Delete ticket

#### Analytics
- **GET** `/statistics` - Dashboard statistics

#### System
- **GET** `/health` - Health check
- **GET** `/` - API information

Full documentation available at: `http://localhost:8000/api/docs`

## 🔧 Configuration

### Backend Environment Variables

```bash
# Application
APP_NAME=AI Support Ticket Triage Agent
DEBUG=False
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite:///./tickets.db
DATABASE_ECHO=False

# Claude AI
CLAUDE_API_KEY=sk-ant-your-key-here
CLAUDE_MODEL=claude-opus-4-1
CLAUDE_MAX_TOKENS=2048
CLAUDE_TIMEOUT=30

# API
API_KEY=  # Optional
ENABLE_CORS=True

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=True
```

### Frontend Environment Variables

```bash
VITE_API_URL=http://localhost:8000
VITE_API_KEY=  # Optional
```

## 📊 Sample Data

Generate sample tickets for testing:

```bash
cd backend
python scripts/generate_sample_data.py
```

This creates 30 diverse sample tickets across all categories.

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::TestClassifyEndpoint::test_classify_valid_ticket -v
```

**Test Coverage:**
- API endpoints (30+ tests)
- Service layer (20+ tests)
- AI agent (15+ tests)
- Database (15+ tests)
- Total: 80+ comprehensive tests

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run with UI
npm run test:ui
```

## 🎨 UI/UX Features

### Dashboard
- Real-time statistics (total, critical, confidence, review)
- Interactive charts (category distribution, urgency breakdown)
- Team workload metrics
- Auto-refresh every 30 seconds

### Ticket Management
- Advanced search across subject and description
- Multi-filter support (urgency, category, status)
- Sortable columns
- Adjustable pagination (10-50 items)
- Quick actions (view, delete)

### Ticket Details
- Complete ticket information
- AI classification breakdown
- Suggested response copy-to-clipboard
- Human review flags
- Status update dropdown
- Reporter contact information
- Timeline visualization

### Dark Mode
- Toggle via header button
- Persists in localStorage
- System preference detection
- Smooth transitions

### Notifications
- Toast notifications (success, error, warning, info)
- Auto-dismiss (4 seconds)
- Manual dismiss option
- Position: bottom-right

## 📁 Project Structure

```
ai-support-ticket-triage/
├── backend/                           # FastAPI backend
│   ├── app/
│   │   ├── api/                      # REST endpoints (14)
│   │   ├── services/                 # Business logic (4)
│   │   ├── models/                   # ORM & schemas
│   │   ├── core/                     # Config & constants
│   │   └── database/                 # DB setup
│   ├── tests/                        # 80+ unit tests
│   ├── main.py                       # Entry point
│   └── requirements.txt               # Dependencies
│
├── frontend/                          # React frontend
│   ├── src/
│   │   ├── components/               # React components
│   │   ├── pages/                    # Page components
│   │   ├── hooks/                    # Custom hooks
│   │   ├── services/                 # API client
│   │   ├── store/                    # Zustand store
│   │   └── types/                    # TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
│
├── docker-compose.yml                 # Multi-container setup
├── README.md                          # This file
└── .gitignore
```

## 🔐 Security

- ✅ Environment-based secrets (no hardcoding)
- ✅ API key authentication (optional)
- ✅ Input validation with Pydantic & React Hook Form
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CORS configuration
- ✅ Non-root Docker user
- ✅ Type safety throughout (TypeScript)
- ✅ Error message sanitization

## 🚨 Error Handling

### Backend
- Comprehensive exception handling
- Meaningful error messages
- HTTP status codes (400, 401, 403, 404, 500)
- Structured error responses
- Logging on all errors

### Frontend
- Toast notifications for errors
- Fallback UI states
- Network error recovery
- Form validation feedback
- Empty states

## 📈 Performance

- Database indices on frequently queried fields
- Pagination for large result sets
- Async database operations
- Connection pooling
- Request deduplication
- Efficient component re-rendering
- Code splitting in frontend

## 🐳 Docker

### Build Images

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Run Stack

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## 📚 API Examples

### Create a Ticket

```bash
curl -X POST http://localhost:8000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Cannot connect to VPN",
    "description": "I have been unable to connect to the company VPN for 2 hours. Error code: 1234",
    "reporter_name": "John Doe",
    "reporter_email": "john.doe@company.com",
    "department": "Sales"
  }'
```

### List Tickets

```bash
# Get first 20 tickets
curl http://localhost:8000/api/tickets?skip=0&limit=20

# Filter by urgency and status
curl 'http://localhost:8000/api/tickets?urgency=High&status=Open'
```

### Get Statistics

```bash
curl http://localhost:8000/api/statistics
```

### Update Status

```bash
curl -X PATCH http://localhost:8000/api/tickets/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

## 🐛 Troubleshooting

### Backend Issues

**Import Error: ModuleNotFoundError**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

**Database Error: "no such table: tickets"**
```bash
# Initialize database
python scripts/init_db.py
```

**Claude API Error: "Invalid API Key"**
```bash
# Check your .env file has correct CLAUDE_API_KEY
cat .env | grep CLAUDE_API_KEY
```

### Frontend Issues

**Port 5173 already in use**
```bash
# Use different port
npm run dev -- --port 3001
```

**API connection refused**
```bash
# Ensure backend is running
curl http://localhost:8000/api/health
```

### Docker Issues

**Container won't start**
```bash
# Check logs
docker-compose logs -f

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🎓 Learning Resources

### AI & Classification
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Claude Documentation](https://docs.anthropic.com/)

### Backend
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

### Frontend
- [React Documentation](https://react.dev/)
- [TailwindCSS](https://tailwindcss.com/)
- [Recharts](https://recharts.org/)

## 📞 Support

- **Issues**: Report via GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: See `docs/` folder

## 🎉 Acknowledgments

Built with ❤️ using:
- [Anthropic Claude API](https://www.anthropic.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [TailwindCSS](https://tailwindcss.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: August 7, 2026

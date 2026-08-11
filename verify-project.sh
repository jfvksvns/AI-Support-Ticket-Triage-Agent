#!/bin/bash

# Project Verification Script
# Checks that all project components are properly set up and working

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

# Functions
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $description"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} $description (not found: $file)"
        ((CHECKS_FAILED++))
    fi
}

check_directory() {
    local dir=$1
    local description=$2
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $description"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} $description (not found: $dir)"
        ((CHECKS_FAILED++))
    fi
}

check_command() {
    local cmd=$1
    local description=$2
    
    if command -v "$cmd" &> /dev/null; then
        local version=$($cmd --version 2>&1 | head -1)
        echo -e "${GREEN}✓${NC} $description ($version)"
        ((CHECKS_PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} $description (not installed)"
        ((CHECKS_WARNING++))
    fi
}

check_docker_running() {
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker daemon running"
        ((CHECKS_PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} Docker daemon not running"
        ((CHECKS_WARNING++))
    fi
}

check_env_variable() {
    local var=$1
    local file=$2
    
    if grep -q "^$var=" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $var configured"
        ((CHECKS_PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} $var not configured in $file"
        ((CHECKS_WARNING++))
    fi
}

# Banner
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        AI Support Ticket Triage Agent - Verification           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Project Structure
echo -e "${BLUE}📁 Project Structure${NC}"
echo "─────────────────────────────────────────────────────────────────"

check_directory "backend" "Backend directory"
check_directory "frontend" "Frontend directory"
check_directory "backend/app" "Backend app package"
check_directory "backend/tests" "Backend tests"
check_directory "frontend/src" "Frontend src directory"

echo ""

# Backend Files
echo -e "${BLUE}📄 Backend Files${NC}"
echo "─────────────────────────────────────────────────────────────────"

check_file "backend/main.py" "Backend entry point"
check_file "backend/requirements.txt" "Python dependencies"
check_file "backend/Dockerfile" "Backend Docker image"
check_file "backend/.env.example" "Environment template"
check_file "backend/app/main.py" "FastAPI application"
check_file "backend/app/api/routes.py" "API routes (14 endpoints)"
check_file "backend/app/services/ai_agent.py" "Claude AI integration"
check_file "backend/app/models/database.py" "Database model"
check_file "backend/app/models/schemas.py" "Validation schemas"

echo ""

# Frontend Files
echo -e "${BLUE}🎨 Frontend Files${NC}"
echo "─────────────────────────────────────────────────────────────────"

check_file "frontend/package.json" "Frontend dependencies"
check_file "frontend/tsconfig.json" "TypeScript configuration"
check_file "frontend/vite.config.ts" "Vite configuration"
check_file "frontend/Dockerfile" "Frontend Docker image"
check_file "frontend/index.html" "HTML entry point"
check_file "frontend/src/main.tsx" "React entry point"
check_file "frontend/src/App.tsx" "Main App component"
check_file "frontend/src/components/TicketForm.tsx" "Ticket form"
check_file "frontend/src/services/api.ts" "API client"

echo ""

# Documentation
echo -e "${BLUE}📚 Documentation${NC}"
echo "─────────────────────────────────────────────────────────────────"

check_file "README.md" "Project README"
check_file "SETUP_GUIDE.md" "Setup guide"
check_file "TESTING_GUIDE.md" "Testing guide"
check_file "TROUBLESHOOTING_FAQ.md" "Troubleshooting FAQ"
check_file "DEPLOYMENT_CHECKLIST.md" "Deployment checklist"
check_file "MIGRATION_GUIDE.md" "Migration guide"
check_file "CONTRIBUTING.md" "Contributing guide"
check_file "PROJECT_AUDIT.md" "Project audit"
check_file "COMPLETION_SUMMARY.md" "Completion summary"

echo ""

# Infrastructure
echo -e "${BLUE}🐳 Infrastructure${NC}"
echo "─────────────────────────────────────────────────────────────────"

check_file "docker-compose.yml" "Docker Compose configuration"
check_file ".gitignore" "Git ignore file"

echo ""

# Tools & Dependencies
echo -e "${BLUE}🛠️  Tools & Dependencies${NC}"
echo "─────────────────────────────────────────────────────────────────"

check_command "python3" "Python"
check_command "node" "Node.js"
check_command "npm" "npm"
check_command "docker" "Docker"
check_command "docker-compose" "Docker Compose"
check_command "git" "Git"

echo ""

# Environment Configuration
echo -e "${BLUE}⚙️  Environment Configuration${NC}"
echo "─────────────────────────────────────────────────────────────────"

if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} Backend .env file exists"
    ((CHECKS_PASSED++))
    
    check_env_variable "CLAUDE_API_KEY" "backend/.env"
    check_env_variable "DATABASE_URL" "backend/.env"
else
    echo -e "${YELLOW}⚠${NC} Backend .env not configured"
    echo "   Run: cd backend && cp .env.example .env && nano .env"
    ((CHECKS_WARNING++))
fi

if [ -f "frontend/.env" ]; then
    echo -e "${GREEN}✓${NC} Frontend .env file exists"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Frontend .env not configured"
    echo "   Run: cd frontend && cp .env.example .env"
    ((CHECKS_WARNING++))
fi

echo ""

# Database
echo -e "${BLUE}💾 Database${NC}"
echo "─────────────────────────────────────────────────────────────────"

if [ -f "backend/tickets.db" ]; then
    echo -e "${GREEN}✓${NC} Database initialized"
    ((CHECKS_PASSED++))
    
    # Check database tables
    if command -v sqlite3 &> /dev/null; then
        TABLES=$(sqlite3 backend/tickets.db ".tables" 2>/dev/null || echo "")
        if [ -n "$TABLES" ]; then
            echo -e "${GREEN}✓${NC} Database tables created"
            ((CHECKS_PASSED++))
        else
            echo -e "${RED}✗${NC} Database empty - run: python backend/scripts/init_db.py"
            ((CHECKS_FAILED++))
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC} Database not initialized"
    echo "   Run: cd backend && python scripts/init_db.py"
    ((CHECKS_WARNING++))
fi

echo ""

# Code Quality
echo -e "${BLUE}✨ Code Quality${NC}"
echo "─────────────────────────────────────────────────────────────────"

# Check for test files
if [ -f "backend/tests/test_api.py" ]; then
    TEST_COUNT=$(grep -c "def test_" backend/tests/*.py 2>/dev/null || echo "0")
    echo -e "${GREEN}✓${NC} Tests implemented ($TEST_COUNT test methods)"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗${NC} Test files missing"
    ((CHECKS_FAILED++))
fi

# Check Python formatting
if command -v black &> /dev/null; then
    echo -e "${GREEN}✓${NC} Black (Python formatter) available"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Black not installed (optional)"
    ((CHECKS_WARNING++))
fi

# Check TypeScript
if [ -f "frontend/tsconfig.json" ]; then
    echo -e "${GREEN}✓${NC} TypeScript configured"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗${NC} TypeScript not configured"
    ((CHECKS_FAILED++))
fi

echo ""

# Runtime Checks
echo -e "${BLUE}🚀 Runtime Checks${NC}"
echo "─────────────────────────────────────────────────────────────────"

# Check if services are running
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend API responding"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Backend API not responding"
    echo "   Start with: cd backend && python main.py"
    ((CHECKS_WARNING++))
fi

if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend dev server responding"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Frontend dev server not responding"
    echo "   Start with: cd frontend && npm run dev"
    ((CHECKS_WARNING++))
fi

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend production server responding"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Frontend production server not responding (expected if not deployed)"
    ((CHECKS_WARNING++))
fi

echo ""

# Docker Checks
echo -e "${BLUE}🐳 Docker Status${NC}"
echo "─────────────────────────────────────────────────────────────────"

check_docker_running

if docker-compose ps 2>/dev/null | grep -q "ticket-triage-backend"; then
    echo -e "${GREEN}✓${NC} Backend container running"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Backend container not running"
    ((CHECKS_WARNING++))
fi

if docker-compose ps 2>/dev/null | grep -q "ticket-triage-frontend"; then
    echo -e "${GREEN}✓${NC} Frontend container running"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Frontend container not running"
    ((CHECKS_WARNING++))
fi

echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    VERIFICATION SUMMARY                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${GREEN}Passed:${NC}   $CHECKS_PASSED"
echo -e "${YELLOW}Warnings:${NC} $CHECKS_WARNING"
echo -e "${RED}Failed:${NC}   $CHECKS_FAILED"

echo ""

# Overall Status
if [ $CHECKS_FAILED -eq 0 ]; then
    if [ $CHECKS_WARNING -eq 0 ]; then
        echo -e "${GREEN}✅ All checks passed! Project is ready.${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Project ready but some warnings present.${NC}"
        echo "   Review warnings above for optional improvements."
        exit 0
    fi
else
    echo -e "${RED}❌ Some checks failed. Review errors above.${NC}"
    exit 1
fi

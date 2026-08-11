#!/bin/bash

# AI Support Ticket Triage Agent - Quick Start Script
# This script sets up and starts the entire project locally

set -e

echo "🚀 AI Support Ticket Triage Agent - Quick Start"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check Node
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"

echo ""
echo -e "${BLUE}🔧 Setting up Backend...${NC}"

# Backend setup
cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env and set CLAUDE_API_KEY${NC}"
fi

# Initialize database
echo "Initializing database..."
python scripts/init_db.py

# Generate sample data (optional)
read -p "Generate sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python scripts/generate_sample_data.py
fi

cd ..

echo -e "${GREEN}✓ Backend setup complete${NC}"

echo ""
echo -e "${BLUE}🎨 Setting up Frontend...${NC}"

cd frontend

# Install dependencies
echo "Installing npm dependencies..."
npm install --silent

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

cd ..

echo -e "${GREEN}✓ Frontend setup complete${NC}"

echo ""
echo -e "${BLUE}🎬 Starting services...${NC}"

# Start backend in background
cd backend
echo "Starting backend server..."
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Backend failed to start${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Backend running on http://localhost:8000${NC}"

cd ..

# Start frontend in background
cd frontend
echo "Starting frontend development server..."
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 5

cd ..

echo ""
echo -e "${GREEN}✅ All services started!${NC}"
echo ""
echo -e "${BLUE}📍 Access Points:${NC}"
echo "   Frontend:        http://localhost:5173"
echo "   Backend API:     http://localhost:8000/api"
echo "   API Swagger:     http://localhost:8000/api/docs"
echo "   API ReDoc:       http://localhost:8000/api/redoc"
echo ""
echo -e "${YELLOW}📝 To stop services:${NC}"
echo "   Backend:  kill $BACKEND_PID"
echo "   Frontend: kill $FRONTEND_PID"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "   • Create a ticket to test the system"
echo "   • Check the dashboard for statistics"
echo "   • Look at API docs for endpoint examples"
echo "   • Sample data includes 30 test tickets"
echo ""
echo "Press Ctrl+C to stop services"

# Wait for services
wait

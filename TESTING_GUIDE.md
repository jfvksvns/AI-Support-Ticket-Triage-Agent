# 🧪 Comprehensive Testing Guide

## Table of Contents
1. [Backend Testing](#backend-testing)
2. [Frontend Testing](#frontend-testing)
3. [Integration Testing](#integration-testing)
4. [Manual Testing](#manual-testing)
5. [Performance Testing](#performance-testing)
6. [CI/CD Pipeline](#cicd-pipeline)

---

## Backend Testing

### Running All Tests

```bash
cd backend

# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run with output
pytest tests/ -v -s

# Run specific test file
pytest tests/test_api.py -v

# Run specific test class
pytest tests/test_api.py::TestCreateTicketEndpoint -v

# Run specific test
pytest tests/test_api.py::TestCreateTicketEndpoint::test_create_valid_ticket -v
```

### Test Files Overview

#### 1. **test_api.py** (30+ tests)
Tests all REST API endpoints

```bash
# Run only API tests
pytest tests/test_api.py -v

# Test classify endpoint
pytest tests/test_api.py::TestClassifyEndpoint -v

# Test ticket creation
pytest tests/test_api.py::TestCreateTicketEndpoint -v

# Test list functionality
pytest tests/test_api.py::TestListTicketsEndpoint -v

# Test filtering
pytest tests/test_api.py::TestListTicketsEndpoint::test_filter_by_urgency -v
```

**Coverage:**
- ✅ POST /classify
- ✅ POST /tickets
- ✅ GET /tickets (with filters)
- ✅ GET /tickets/{id}
- ✅ PATCH /tickets/{id}/status
- ✅ DELETE /tickets/{id}
- ✅ GET /statistics
- ✅ GET /health
- ✅ Error handling

#### 2. **test_services.py** (20+ tests)
Tests business logic services

```bash
# Run service tests
pytest tests/test_services.py -v

# Test ticket service
pytest tests/test_services.py::TestTicketService -v

# Test classification service
pytest tests/test_services.py::TestClassificationService -v

# Test analytics service
pytest tests/test_services.py::TestAnalyticsService -v
```

**Coverage:**
- ✅ Create tickets
- ✅ Read tickets (single/list)
- ✅ Update status
- ✅ Delete tickets
- ✅ Search functionality
- ✅ Filtering logic
- ✅ Statistics calculation
- ✅ Team distribution

#### 3. **test_ai_agent.py** (15+ tests)
Tests Claude AI integration

```bash
# Run AI agent tests
pytest tests/test_ai_agent.py -v

# Test classification
pytest tests/test_ai_agent.py::TestAIAgentService::test_classify_ticket -v

# Test response parsing
pytest tests/test_ai_agent.py::TestResponseParsing -v

# Test validation
pytest tests/test_ai_agent.py::TestResponseParsing::test_parse_valid_response -v
```

**Coverage:**
- ✅ Ticket classification
- ✅ Response parsing
- ✅ JSON validation
- ✅ Confidence scoring
- ✅ Category validation
- ✅ Urgency validation
- ✅ Error handling
- ✅ Markdown parsing

#### 4. **test_database.py** (15+ tests)
Tests database models and operations

```bash
# Run database tests
pytest tests/test_database.py -v

# Test model validation
pytest tests/test_database.py::TestTicketModel -v

# Test constraints
pytest tests/test_database.py::TestDatabaseConstraints -v

# Test indices
pytest tests/test_database.py::TestDatabaseIndices -v
```

**Coverage:**
- ✅ Model creation
- ✅ Field validation
- ✅ Constraints
- ✅ Unique fields
- ✅ Timestamps
- ✅ Indices
- ✅ Relationships

### Test Examples

#### Creating a Test

```python
def test_create_valid_ticket(test_client, sample_ticket_data):
    """Test creating a valid ticket."""
    response = test_client.post("/api/tickets", json=sample_ticket_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["subject"] == sample_ticket_data["subject"]
    assert "id" in data
```

#### Testing with Fixtures

```python
@pytest.fixture
def sample_ticket_data():
    """Sample ticket data for testing."""
    return {
        "subject": "Test Issue",
        "description": "Test description",
        "reporter_name": "John Doe",
        "reporter_email": "john@example.com",
        "department": "IT"
    }
```

### Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html

# View report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

---

## Frontend Testing

### Running Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test -- --coverage

# Watch mode
npm run test -- --watch
```

### Setting Up Frontend Tests

Add to package.json:

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

### Example Frontend Test

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Header } from '@/components/Header'

describe('Header', () => {
  it('renders navigation links', () => {
    render(<Header />)
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Tickets')).toBeInTheDocument()
  })

  it('toggles dark mode', () => {
    render(<Header />)
    
    const toggleButton = screen.getByLabelText('Toggle dark mode')
    fireEvent.click(toggleButton)
    
    expect(document.documentElement).toHaveClass('dark')
  })
})
```

---

## Integration Testing

### End-to-End Workflow Test

Test the complete ticket lifecycle:

```bash
# 1. Start backend
cd backend && python main.py &

# 2. Start frontend
cd frontend && npm run dev &

# 3. Run integration tests
pytest tests/test_integration.py -v
```

### Manual Integration Test

```bash
# 1. Create ticket via API
curl -X POST http://localhost:8000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Issue",
    "description": "Test description for classification",
    "reporter_name": "Test User",
    "reporter_email": "test@example.com",
    "department": "IT"
  }'

# Response should include classification:
# {
#   "id": 1,
#   "subject": "Test Issue",
#   "category": "Software",
#   "urgency": "Medium",
#   "confidence": 85,
#   ...
# }

# 2. List tickets
curl http://localhost:8000/api/tickets

# 3. Get statistics
curl http://localhost:8000/api/statistics

# 4. Update status
curl -X PATCH http://localhost:8000/api/tickets/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'

# 5. Get details
curl http://localhost:8000/api/tickets/1
```

---

## Manual Testing

### Test Scenarios

#### Scenario 1: Create and Classify Ticket
1. Open http://localhost:3000
2. Click "New Ticket"
3. Fill form:
   - Subject: "Cannot connect to email"
   - Description: "Outlook not syncing emails since this morning"
   - Name: "Test User"
   - Email: "test@example.com"
   - Department: "Sales"
4. Click "Create Ticket"
5. Verify redirect to ticket details
6. Verify AI classification shows:
   - Category: "Email"
   - Urgency: "Medium" or "High"
   - Confidence: >70%

#### Scenario 2: Search and Filter
1. Go to "Tickets" page
2. Search: "email"
   - Should show email-related tickets
3. Filter by Urgency: "High"
   - Should show only high-urgency tickets
4. Filter by Category: "Network"
   - Should update list accordingly
5. Sort by Confidence
   - Should reorder by confidence score

#### Scenario 3: Update Status
1. Click on any ticket
2. Click Status dropdown
3. Select "In Progress"
4. Verify status updated immediately
5. Go back to list
6. Verify status persists

#### Scenario 4: Dark Mode
1. Click moon icon in header
2. Verify entire UI switches to dark mode
3. Refresh page
4. Verify dark mode persists
5. Click sun icon
6. Verify light mode restored

#### Scenario 5: Notifications
1. Create a new ticket
2. Verify success toast appears
3. Wait 4 seconds
4. Verify toast auto-dismisses
5. Try deleting a ticket
6. Click cancel on confirmation
7. Verify no deletion toast appears

#### Scenario 6: Pagination
1. Go to Tickets
2. Click "50 per page"
3. Verify page size changes
4. Click next page button
5. Verify new tickets load
6. Click previous page button
7. Verify back on first page

#### Scenario 7: Statistics
1. Go to Dashboard
2. Verify all stat cards load
3. Verify charts render correctly
4. Wait 30 seconds
5. Verify data auto-refreshes
6. Check pie chart is interactive
7. Check bar chart displays urgency distribution

#### Scenario 8: Copy Response
1. Open any ticket details
2. Find "Suggested Response" section
3. Click "Copy response"
4. Verify toast notification
5. Paste (Ctrl+V) somewhere
6. Verify response text is copied

---

## Performance Testing

### Load Testing

```bash
# Install ab (Apache Bench)
sudo apt-get install apache2-utils  # Linux
# or
brew install httpd  # macOS

# Test backend endpoints
ab -n 1000 -c 10 http://localhost:8000/api/health

# Test with POST data
ab -n 100 -c 5 -p data.json -T application/json \
  http://localhost:8000/api/classify
```

### Memory Profiling

```bash
# Backend
pip install memory-profiler

# Run with memory profiling
python -m memory_profiler backend/main.py

# Frontend
npm install --save-dev @testing-library/performance
```

### Response Time Testing

```bash
# Test endpoint response times
for i in {1..10}; do
  curl -w "Time: %{time_total}s\n" \
    http://localhost:8000/api/tickets
done
```

---

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/ --cov=app
  
  frontend:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      
      - name: Run tests
        run: |
          cd frontend
          npm run test
      
      - name: Build
        run: |
          cd frontend
          npm run build
```

### Pre-commit Hooks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Run backend tests
cd backend
pytest tests/ -q
if [ $? -ne 0 ]; then
    echo "Backend tests failed!"
    exit 1
fi

# Run frontend tests
cd ../frontend
npm run test -- --run
if [ $? -ne 0 ]; then
    echo "Frontend tests failed!"
    exit 1
fi

exit 0
```

---

## Troubleshooting Tests

### Common Issues

**Tests fail with database error:**
```bash
# Clear database
rm backend/tickets.db
pytest tests/ -v
```

**Import errors:**
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Mock API failures:**
```bash
# Check CLAUDE_API_KEY in .env
cat backend/.env | grep CLAUDE_API_KEY

# Tests use mocks, so key not needed for tests
```

---

## Test Checklist

### Backend Testing
- [ ] All 80+ tests pass
- [ ] Coverage >80%
- [ ] No warnings
- [ ] All endpoints tested
- [ ] Error scenarios tested
- [ ] Database operations tested
- [ ] AI agent tested with mocks

### Frontend Testing  
- [ ] Components render
- [ ] Forms validate
- [ ] Navigation works
- [ ] Dark mode toggles
- [ ] Notifications appear
- [ ] API calls succeed
- [ ] Error states handled

### Integration Testing
- [ ] Create ticket end-to-end
- [ ] Search and filter work
- [ ] Status updates persist
- [ ] Statistics accurate
- [ ] Dark mode persists
- [ ] Pagination works
- [ ] Charts render

### Manual Testing
- [ ] UI looks professional
- [ ] Responsive on mobile
- [ ] No console errors
- [ ] No visual glitches
- [ ] Forms intuitive
- [ ] Error messages clear
- [ ] Performance acceptable

---

**Testing Status**: ✅ Comprehensive  
**Test Coverage**: >80%  
**Test Count**: 80+  
**Automated**: Yes  
**CI/CD Ready**: Yes

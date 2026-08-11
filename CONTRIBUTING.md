# 🤝 Contributing Guide

Thank you for your interest in contributing to the AI Support Ticket Triage Agent!

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Standards](#code-standards)
4. [Testing](#testing)
5. [Submitting Changes](#submitting-changes)
6. [Reporting Issues](#reporting-issues)

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Claude API key (for testing)
- Git

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/ai-ticket-triage.git
cd ai-ticket-triage

# Create feature branch
git checkout -b feature/your-feature-name

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings

# Setup frontend
cd ../frontend
npm install
cp .env.example .env
```

---

## Development Workflow

### 1. Choose an Issue
```bash
# Look for issues tagged:
# - good first issue
# - help wanted
# - enhancement
```

### 2. Create Feature Branch
```bash
# Use descriptive branch names
git checkout -b feature/add-email-notifications
git checkout -b fix/classify-endpoint-timeout
git checkout -b docs/update-api-examples
```

### 3. Make Changes

#### Backend Changes
```bash
# Follow Python conventions
# - Use type hints
# - Add docstrings
# - Follow PEP 8

# Example:
def classify_ticket(
    subject: str,
    description: str
) -> ClassificationResponse:
    """
    Classify a support ticket using Claude AI.
    
    Args:
        subject: Ticket subject line
        description: Detailed ticket description
        
    Returns:
        ClassificationResponse with category, urgency, etc.
        
    Raises:
        ValueError: If subject or description empty
        APIError: If Claude API fails
    """
```

#### Frontend Changes
```typescript
// Follow TypeScript conventions
// - Use type safety
// - Add JSDoc comments
// - Use component composition

// Example:
interface TicketFormProps {
  onSubmit: (data: TicketData) => Promise<void>
  isLoading?: boolean
}

/**
 * Ticket creation form component
 * Handles form validation and submission
 */
export function TicketForm({ onSubmit, isLoading }: TicketFormProps) {
  // Component code
}
```

### 4. Write Tests

#### Backend Tests
```python
# Add tests to backend/tests/

def test_classify_valid_ticket(test_client):
    """Test classifying a valid ticket."""
    response = test_client.post(
        "/api/classify",
        json={
            "subject": "Cannot connect to email",
            "description": "Outlook not syncing"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "category" in data["classification"]
    assert "urgency" in data["classification"]
```

#### Frontend Tests
```typescript
// Add tests for new components

import { render, screen } from '@testing-library/react'
import { NewComponent } from '@/components/NewComponent'

describe('NewComponent', () => {
  it('renders correctly', () => {
    render(<NewComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })
  
  it('handles user interaction', () => {
    render(<NewComponent />)
    // Test interactions
  })
})
```

### 5. Run Tests Locally
```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm run test

# Both with coverage
cd backend && pytest tests/ --cov=app
cd ../frontend && npm run test -- --coverage
```

### 6. Commit Changes

```bash
# Write clear commit messages
git add .
git commit -m "feat: add email notification support"

# Follow conventional commits:
# feat: new feature
# fix: bug fix
# docs: documentation
# style: formatting
# refactor: code reorganization
# test: test additions
# chore: maintenance
```

### 7. Push and Create PR
```bash
git push origin feature/your-feature-name

# Create PR on GitHub
# - Describe changes
# - Reference related issues
# - Mention reviewers if needed
```

---

## Code Standards

### Backend (Python)

#### Naming Conventions
```python
# Functions and variables: snake_case
def classify_ticket():
    pass

ticket_id = 1
urgency_level = "High"

# Classes: PascalCase
class TicketService:
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
```

#### Type Hints
```python
from typing import List, Optional, Dict
from app.models.schemas import Ticket

def get_tickets(
    skip: int = 0,
    limit: int = 50,
    urgency: Optional[str] = None
) -> List[Ticket]:
    """Get tickets with optional filtering."""
    pass
```

#### Docstrings
```python
def create_ticket(data: TicketCreateRequest) -> Ticket:
    """
    Create a new support ticket.
    
    Args:
        data: Ticket data including subject, description, reporter info
        
    Returns:
        Created Ticket with AI classification
        
    Raises:
        ValueError: If required fields missing
        APIError: If AI classification fails
        
    Example:
        >>> response = create_ticket(ticket_data)
        >>> print(response.category)
        'Software'
    """
```

#### Code Style
```python
# Use black formatter
black backend/

# Use isort for imports
isort backend/

# Lint with pylint/flake8
flake8 backend/ --max-line-length=100
```

### Frontend (TypeScript/React)

#### Naming Conventions
```typescript
// Components: PascalCase
function TicketForm() {}

// Functions: camelCase
const handleSubmit = () => {}

// Interfaces: PascalCase, prefixed with I (optional)
interface ITicketFormProps {}

// Constants: UPPER_SNAKE_CASE
const MAX_UPLOAD_SIZE = 10 * 1024 * 1024
```

#### Type Safety
```typescript
// Always type props
interface ComponentProps {
  ticketId: number
  onUpdate: (status: string) => void
  isLoading?: boolean
}

// Always type function returns
function getValue(key: string): string | null {
  return null
}

// Use enums for constants
enum TicketStatus {
  Open = 'Open',
  InProgress = 'In Progress',
  Closed = 'Closed'
}
```

#### Component Structure
```typescript
// Group imports
import React, { useState } from 'react'
import { useApi } from '@/hooks/useApi'
import { Button } from '@/components/Button'
import { styles } from './Component.module.css'

// Props interface
interface ComponentProps {
  prop1: string
}

// Component
export function Component({ prop1 }: ComponentProps) {
  // Hooks first
  const [state, setState] = useState('')
  const { data } = useApi()
  
  // Effects
  useEffect(() => {
    // Effects code
  }, [])
  
  // Handlers
  const handleClick = () => {}
  
  // Render
  return <div>{prop1}</div>
}
```

#### Formatting
```bash
# Format code with Prettier
npm run format

# Or configure pre-commit hook
```

---

## Testing Standards

### Backend Test Structure
```python
import pytest
from app.models.database import Ticket

class TestTicketService:
    """Test suite for TicketService."""
    
    def test_create_valid_ticket(self, test_client, sample_data):
        """Test creating a ticket with valid data."""
        # Arrange
        expected_status = 201
        
        # Act
        response = test_client.post("/api/tickets", json=sample_data)
        
        # Assert
        assert response.status_code == expected_status
        assert response.json()["id"] is not None
    
    def test_create_invalid_ticket(self, test_client):
        """Test creating a ticket with invalid data."""
        # Should raise validation error
        response = test_client.post("/api/tickets", json={})
        assert response.status_code == 422
```

### Frontend Test Structure
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('Component', () => {
  it('renders with correct content', () => {
    // Arrange
    const props = { /* test props */ }
    
    // Act
    render(<Component {...props} />)
    
    // Assert
    expect(screen.getByText('Expected')).toBeInTheDocument()
  })
  
  it('handles user interaction', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<Component />)
    
    // Act
    await user.click(screen.getByRole('button'))
    
    // Assert
    expect(screen.getByText('Updated')).toBeInTheDocument()
  })
})
```

### Coverage Requirements
- Minimum 80% code coverage
- All public functions tested
- All error paths tested
- Happy path and sad paths

---

## Submitting Changes

### Pre-Submission Checklist
- [ ] Code follows style guide
- [ ] Added/updated tests
- [ ] Tests pass locally
- [ ] No console errors/warnings
- [ ] Commits are clean
- [ ] Commit messages clear
- [ ] No unrelated changes
- [ ] Documentation updated

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## How to Test
Steps to test the changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Fixes #issue_number

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Code reviewed locally
```

### Code Review Process
1. Automatic checks (tests, linting)
2. At least 1 maintainer review
3. Request changes if needed
4. Approval and merge

---

## Reporting Issues

### Bug Reports
Use template:
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Expected result
4. Actual result

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.0]
- Node: [e.g., 18.12.0]
- Browser: [e.g., Chrome 108]

## Logs
Include relevant error messages

## Screenshots
If applicable
```

### Feature Requests
Use template:
```markdown
## Description
What you'd like implemented

## Use Case
Why you need this feature

## Suggested Implementation
How you think it should work

## Alternatives
Any alternatives considered
```

---

## Development Tips

### Local Development
```bash
# Watch mode for tests
pytest tests/ -v --tb=short -s -k "test_name"

# Frontend hot reload
npm run dev

# Backend debug logging
LOG_LEVEL=DEBUG python main.py
```

### Debugging
```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use debugger
python -m pdb backend/main.py
```

```typescript
// Add browser debugging
debugger;

// Or use console
console.log('Debug:', variable)
```

### Performance Testing
```bash
# Load test
ab -n 1000 -c 10 http://localhost:8000/api/health

# Memory profiling
python -m memory_profiler backend/main.py
```

---

## Documentation Guidelines

### Code Comments
```python
# Good: Explains why, not what
# We use exponential backoff to handle rate limiting
def retry_with_backoff(func, max_retries=3):
    pass

# Bad: Obvious what code does
# Increment counter
counter += 1
```

### Docstring Format
Follow Google style:
```python
def function(param1: str, param2: int) -> bool:
    """
    Summary line.
    
    Longer description if needed.
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Description
        
    Raises:
        ExceptionType: When this occurs
        
    Example:
        >>> function("test", 1)
        True
    """
```

### README Updates
- Update if adding new features
- Update if changing workflows
- Update if adding new endpoints
- Include examples and screenshots

---

## Community Guidelines

### Be Respectful
- Treat everyone with respect
- Welcome different opinions
- Provide constructive feedback
- Be patient with questions

### Stay On Topic
- Keep discussions relevant
- Use threads for conversations
- Search before asking
- Avoid spam/promotion

### Report Issues Appropriately
- Use GitHub issues for bugs
- Use discussions for questions
- Email maintainers for security issues
- Don't report publicly

---

## Recognized Contributors

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

---

## Questions?

- Check existing documentation
- Search closed issues
- Ask in discussions
- Email maintainers

---

**Thank you for contributing! 🙏**

We appreciate your help making this project better.

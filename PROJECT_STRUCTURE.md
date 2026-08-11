# AI Support Ticket Triage Agent - Complete Project Structure

## Root Folder Structure

```
ai-support-triage-agent/
├── backend/                          # FastAPI Python backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── config.py                 # Configuration management
│   │   ├── models.py                 # Pydantic models (requests/responses)
│   │   ├── schemas.py                # SQLAlchemy database schemas
│   │   ├── database.py               # Database connection & session
│   │   ├── dependencies.py           # FastAPI dependencies
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── tickets.py            # Ticket CRUD endpoints
│   │   │   ├── classify.py           # AI classification endpoint
│   │   │   ├── statistics.py         # Analytics endpoints
│   │   │   ├── health.py             # Health check endpoint
│   │   │   └── middleware.py         # Request/response middleware
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── triage_agent.py       # Main AI triage logic
│   │   │   ├── prompts.py            # System prompts & templates
│   │   │   ├── validators.py         # Output validation
│   │   │   └── llm_client.py         # Claude API client
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ticket_service.py     # Business logic for tickets
│   │   │   ├── classification_service.py  # Classification logic
│   │   │   ├── analytics_service.py  # Analytics aggregation
│   │   │   └── email_service.py      # Email notifications (future)
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py             # Logging setup
│   │       ├── errors.py             # Custom exception classes
│   │       └── helpers.py            # Utility functions
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py               # Pytest configuration
│   │   ├── test_models.py            # Pydantic model tests
│   │   ├── test_database.py          # Database operation tests
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── test_tickets.py       # Ticket endpoint tests
│   │   │   ├── test_classify.py      # Classification endpoint tests
│   │   │   └── test_statistics.py    # Analytics endpoint tests
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── test_triage_agent.py  # Agent logic tests
│   │   │   ├── test_validators.py    # Validation tests
│   │   │   └── test_llm_client.py    # LLM client mock tests
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── test_ticket_service.py
│   │       └── test_classification_service.py
│   │
│   ├── data/
│   │   ├── sample_tickets.json       # 30 sample tickets
│   │   └── seed_database.py          # Database seed script
│   │
│   ├── logs/                         # Log files (gitignored)
│   ├── .env.example                  # Environment variables template
│   ├── requirements.txt              # Python dependencies
│   └── README.md                     # Backend README

├── frontend/                         # React + TypeScript frontend
│   ├── src/
│   │   ├── index.tsx                 # React entry point
│   │   ├── App.tsx                   # Main app component
│   │   ├── main.tsx                  # Vite entry
│   │   │
│   │   ├── components/
│   │   │   ├── Dashboard.tsx         # Main dashboard page
│   │   │   ├── TicketForm.tsx        # Ticket submission form
│   │   │   ├── TicketList.tsx        # List of all tickets
│   │   │   ├── TicketDetail.tsx      # Single ticket view
│   │   │   │
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx        # App header/navbar
│   │   │   │   ├── Sidebar.tsx       # Navigation sidebar
│   │   │   │   ├── Toast.tsx         # Notification component
│   │   │   │   ├── LoadingSpinner.tsx # Loading indicator
│   │   │   │   ├── ErrorBoundary.tsx # Error handling
│   │   │   │   └── Modal.tsx         # Modal dialog
│   │   │   │
│   │   │   ├── cards/
│   │   │   │   ├── StatsCard.tsx     # Statistics card
│   │   │   │   ├── TicketCard.tsx    # Ticket summary card
│   │   │   │   └── PriorityBadge.tsx # Priority indicator
│   │   │   │
│   │   │   └── charts/
│   │   │       ├── CategoryPieChart.tsx    # Category distribution
│   │   │       ├── UrgencyBarChart.tsx     # Urgency breakdown
│   │   │       └── TicketsPerDayChart.tsx  # Ticket trends
│   │   │
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx     # Dashboard page wrapper
│   │   │   ├── SubmitTicketPage.tsx  # Form submission page
│   │   │   ├── TicketsHistoryPage.tsx # Tickets list page
│   │   │   └── NotFoundPage.tsx      # 404 page
│   │   │
│   │   ├── hooks/
│   │   │   ├── useTickets.ts         # Tickets API hook
│   │   │   ├── useClassification.ts  # Classification API hook
│   │   │   ├── useToast.ts           # Toast notification hook
│   │   │   ├── useDarkMode.ts        # Dark mode hook
│   │   │   └── useForm.ts            # Form state management
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts                # Axios API client
│   │   │   ├── ticketService.ts      # Ticket API methods
│   │   │   ├── classificationService.ts  # Classification API
│   │   │   └── statsService.ts       # Statistics API
│   │   │
│   │   ├── types/
│   │   │   ├── index.ts              # Type definitions
│   │   │   ├── ticket.ts             # Ticket types
│   │   │   ├── agent.ts              # Agent response types
│   │   │   └── api.ts                # API response types
│   │   │
│   │   ├── utils/
│   │   │   ├── formatters.ts         # Text formatting utilities
│   │   │   ├── validators.ts         # Form validation
│   │   │   ├── colors.ts             # Color/category mapping
│   │   │   └── constants.ts          # App constants
│   │   │
│   │   ├── styles/
│   │   │   ├── index.css             # Global styles
│   │   │   ├── dashboard.css         # Dashboard styles
│   │   │   ├── form.css              # Form styles
│   │   │   └── responsive.css        # Mobile responsive
│   │   │
│   │   └── store/ (optional Redux)
│   │       ├── ticketSlice.ts
│   │       ├── statsSlice.ts
│   │       └── store.ts
│   │
│   ├── public/
│   │   └── favicon.svg               # App icon
│   │
│   ├── tests/
│   │   ├── setup.ts                  # Test configuration
│   │   ├── components.test.tsx       # Component tests
│   │   ├── hooks.test.ts             # Hook tests
│   │   └── services.test.ts          # Service tests
│   │
│   ├── .env.example                  # Environment template
│   ├── package.json                  # NPM dependencies
│   ├── vite.config.ts                # Vite configuration
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.js            # Tailwind CSS config
│   ├── postcss.config.js             # PostCSS config
│   └── README.md                     # Frontend README

├── docker/
│   ├── Dockerfile.backend            # Backend Docker image
│   ├── Dockerfile.frontend           # Frontend Docker image
│   └── nginx.conf                    # Nginx reverse proxy config

├── docker-compose.yml                # Multi-container orchestration
├── .gitignore                        # Git ignore rules
├── .github/
│   └── workflows/
│       ├── backend-tests.yml         # CI/CD for backend
│       └── frontend-tests.yml        # CI/CD for frontend

├── README.md                         # Project root README
├── ARCHITECTURE.md                   # Architecture documentation
├── API_DOCUMENTATION.md              # API specs & examples
├── DESIGN_DECISIONS.md               # Technical decisions log
└── DEVELOPMENT_ROADMAP.md            # Feature roadmap

```

## Directory Purposes

### Backend (`/backend`)
- **app/**: Core application code
  - `api/`: REST API endpoints
  - `agents/`: AI triage logic & LLM integration
  - `services/`: Business logic layer
  - `utils/`: Shared utilities & helpers
- **tests/**: Complete test suite
- **data/**: Sample data & seeding scripts
- **requirements.txt**: Python package dependencies

### Frontend (`/frontend`)
- **src/components/**: Reusable React components
- **src/pages/**: Full page components
- **src/hooks/**: Custom React hooks
- **src/services/**: API client layer
- **src/types/**: TypeScript type definitions
- **src/styles/**: Tailwind CSS & custom styles
- **public/**: Static assets
- **tests/**: Jest/Vitest test suite

### Docker
- Containerization for both services
- Nginx reverse proxy configuration
- Docker Compose for local orchestration

### Documentation
- README files at each level
- Architecture diagrams
- API documentation with examples
- Design decision log

## File Naming Conventions

### Python Files
- `models.py` - Pydantic data models
- `schemas.py` - SQLAlchemy ORM models
- `services.py` - Business logic
- `routes.py` / `endpoints.py` - API routes
- `test_*.py` - Test files

### TypeScript/React Files
- `*.tsx` - React components
- `*.ts` - TypeScript utilities/services
- `*.test.tsx` / `*.test.ts` - Test files
- `*Hook.ts` - Custom hooks

### Configuration Files
- `.env` - Environment variables (not committed)
- `.env.example` - Template (committed)
- `config.py` - Backend configuration
- `tsconfig.json` - TypeScript configuration

## Key Design Principles

1. **Separation of Concerns**: API layer, service layer, data layer
2. **Type Safety**: TypeScript on frontend, type hints on backend
3. **Testing**: Unit tests for business logic, integration tests for APIs
4. **Documentation**: Self-documenting code with clear comments
5. **Scalability**: Ready for future features and load
6. **Security**: Input validation, error handling, secure defaults

# 📦 Migration Guide: Integrating with Existing Systems

## Overview

This guide helps migrate from existing ticket management systems to the AI Support Ticket Triage Agent.

---

## Pre-Migration Planning

### Step 1: Assessment
- [ ] Document current system architecture
- [ ] Identify data structure in existing system
- [ ] Calculate data volume (ticket count, attachments, etc.)
- [ ] Identify integration points
- [ ] Plan maintenance window
- [ ] Backup existing system

### Step 2: Mapping
Create a mapping of your current system to the new system:

```
Existing System          →    New System
================              ===========
ticket_id               →    id
title                   →    subject
description             →    description
created_by              →    reporter_name
created_by_email        →    reporter_email
department              →    department
priority                →    urgency (needs mapping)
category_code           →    category (needs mapping)
status                  →    status
assignment              →    assigned_team (AI-determined)
notes                   →    reasoning (AI-generated)
custom_fields           →    JSON metadata (optional)
created_at              →    created_at
updated_at              →    updated_at
```

### Step 3: Risk Assessment
- [ ] Data compatibility issues
- [ ] Downtime impact
- [ ] Rollback procedures
- [ ] Training requirements
- [ ] Support resources needed

---

## Data Migration

### Option 1: Direct SQL Migration

For systems with SQL databases, create migration scripts:

#### Step 1: Extract Data

```python
import sqlite3
import json
from datetime import datetime

# Export from existing system
existing_db = sqlite3.connect('existing_tickets.db')
cursor = existing_db.cursor()

# Query existing tickets
cursor.execute("""
    SELECT 
        id, title, description, created_by, created_by_email,
        department, priority, category, status, created_at, updated_at
    FROM tickets
""")

tickets = cursor.fetchall()
existing_db.close()

# Convert to new format
migrated_tickets = []
priority_map = {
    1: 'Low',
    2: 'Medium', 
    3: 'High',
    4: 'Critical'
}

category_map = {
    'hw': 'Hardware',
    'sw': 'Software',
    'net': 'Network',
    'sec': 'Security',
    # ... add your mappings
}

for ticket in tickets:
    migrated = {
        'id': ticket[0],
        'subject': ticket[1],
        'description': ticket[2],
        'reporter_name': ticket[3],
        'reporter_email': ticket[4],
        'department': ticket[5],
        'urgency': priority_map.get(ticket[6], 'Medium'),
        'category': category_map.get(ticket[7], 'Other'),
        'status': ticket[8],
        'created_at': ticket[9],
        'updated_at': ticket[10],
    }
    migrated_tickets.append(migrated)

# Save to JSON for import
with open('migrated_tickets.json', 'w') as f:
    json.dump(migrated_tickets, f, indent=2)
```

#### Step 2: Import Data

```python
from app.models.database import Ticket
from app.database.engine import DatabaseEngine
import json

# Initialize target database
DatabaseEngine.initialize()
session = DatabaseEngine.get_session()

# Load migrated data
with open('migrated_tickets.json', 'r') as f:
    migrated_tickets = json.load(f)

# Import tickets
for data in migrated_tickets:
    ticket = Ticket(
        subject=data['subject'],
        description=data['description'],
        reporter_name=data['reporter_name'],
        reporter_email=data['reporter_email'],
        department=data['department'],
        category=data['category'],
        urgency=data['urgency'],
        status=data['status'],
        confidence=70,  # Default confidence
        assigned_team='Service Desk',  # Will be updated by AI
        summary='Migrated from legacy system',
        reasoning='Historical ticket from migration',
        suggested_response='Please contact support',
        requires_human_review=True,  # Review all migrated
        created_at=data['created_at'],
        updated_at=data['updated_at']
    )
    session.add(ticket)

session.commit()
session.close()

print(f"✓ Migrated {len(migrated_tickets)} tickets")
```

### Option 2: CSV Import

For spreadsheet-based systems:

#### Step 1: Prepare CSV

```csv
subject,description,reporter_name,reporter_email,department,urgency,category,status
Cannot connect to email,Outlook stopped syncing,John Doe,john@example.com,Sales,High,Email,Open
Database slow,Queries taking 2 minutes,Jane Smith,jane@example.com,IT,Critical,Database,In Progress
```

#### Step 2: Import Script

```python
import csv
from app.models.database import Ticket
from app.database.engine import DatabaseEngine
from datetime import datetime

DatabaseEngine.initialize()
session = DatabaseEngine.get_session()

with open('tickets.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        ticket = Ticket(
            subject=row['subject'],
            description=row['description'],
            reporter_name=row['reporter_name'],
            reporter_email=row['reporter_email'],
            department=row['department'],
            category=row['category'],
            urgency=row['urgency'],
            status=row['status'],
            confidence=70,
            assigned_team='Service Desk',
            summary=f"Migrated: {row['subject'][:100]}",
            reasoning='Imported from legacy system',
            suggested_response='Ticket imported. Please review.',
            requires_human_review=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(ticket)

session.commit()
session.close()
print("✓ Import complete")
```

### Option 3: API-Based Migration

For systems with APIs:

```python
import requests
import time
from app.database.engine import DatabaseEngine
from app.models.database import Ticket

# Connect to existing system API
existing_api_url = "https://existing-system.com/api"
existing_api_key = "your-api-key"

headers = {"Authorization": f"Bearer {existing_api_key}"}

# Fetch all tickets
response = requests.get(
    f"{existing_api_url}/tickets",
    headers=headers,
    params={"limit": 1000}
)

if response.status_code != 200:
    raise Exception(f"API error: {response.text}")

tickets_data = response.json()['data']

# Initialize new system
DatabaseEngine.initialize()
session = DatabaseEngine.get_session()

# Migrate to new system
for ticket_data in tickets_data:
    ticket = Ticket(
        subject=ticket_data['title'],
        description=ticket_data['description'],
        reporter_name=ticket_data['reporter'],
        reporter_email=ticket_data['reporter_email'],
        department=ticket_data.get('department', 'General'),
        category=ticket_data.get('category', 'Other'),
        urgency=ticket_data.get('priority', 'Medium'),
        status=ticket_data.get('status', 'Open'),
        confidence=70,
        assigned_team='Service Desk',
        summary=ticket_data['title'][:255],
        reasoning='Migrated from legacy system',
        suggested_response='This ticket was imported. Please review.',
        requires_human_review=True,
        created_at=ticket_data.get('created_at'),
        updated_at=ticket_data.get('updated_at')
    )
    session.add(ticket)
    
    # Commit in batches
    if tickets_data.index(ticket_data) % 100 == 0:
        session.commit()
        print(f"✓ Migrated {tickets_data.index(ticket_data)} tickets")
        time.sleep(1)  # Rate limiting

session.commit()
session.close()
print(f"✓ Migrated {len(tickets_data)} tickets total")
```

---

## Integration Steps

### Step 1: Pre-Migration Backup
```bash
# Backup existing system
mysqldump existing_db > existing_db_backup.sql
# or
pg_dump existing_db > existing_db_backup.sql

# Backup to file
cp existing_db.db existing_db.backup
```

### Step 2: Set Up New System
```bash
# Setup new system on parallel infrastructure
docker-compose up -d

# Verify system healthy
curl http://localhost:8000/api/health
```

### Step 3: Run Migration
```bash
# Run your chosen migration script
python migrate_sql.py
# or
python migrate_csv.py
# or
python migrate_api.py

# Verify import
curl http://localhost:8000/api/statistics
```

### Step 4: Validate Data
```bash
# Check ticket counts
SELECT COUNT(*) FROM tickets;  -- Should match source

# Check data quality
SELECT COUNT(*) FROM tickets WHERE urgency IS NULL;
SELECT COUNT(*) FROM tickets WHERE category IS NULL;
SELECT COUNT(*) FROM tickets WHERE status IS NULL;
```

### Step 5: User Training
- [ ] Train support team on new UI
- [ ] Explain classification system
- [ ] Demo search and filter
- [ ] Show API capabilities
- [ ] Review statistics dashboard

### Step 6: Cutover
- [ ] Schedule maintenance window
- [ ] Notify users
- [ ] Stop old system
- [ ] Switch DNS/load balancer
- [ ] Monitor new system
- [ ] Document any issues

---

## Post-Migration Validation

### Checklist

```bash
# 1. Data integrity
curl http://localhost:8000/api/statistics

# 2. Random spot check
curl http://localhost:8000/api/tickets/1
curl http://localhost:8000/api/tickets/100
curl http://localhost:8000/api/tickets/1000

# 3. Search functionality
curl "http://localhost:8000/api/tickets?search=email"

# 4. Filtering
curl "http://localhost:8000/api/tickets?urgency=High"

# 5. Classification accuracy
# Review AI classifications on sample of migrated tickets

# 6. Performance
time curl http://localhost:8000/api/tickets
# Should return in <1 second

# 7. User access
# Test login and permissions
# Verify user data preserved
```

### Validation Script

```python
from app.database.engine import DatabaseEngine

DatabaseEngine.initialize()
session = DatabaseEngine.get_session()

# Check ticket counts
total = session.query(Ticket).count()
print(f"Total tickets: {total}")

# Check distribution
from sqlalchemy import func
categories = session.query(
    Ticket.category,
    func.count(Ticket.id)
).group_by(Ticket.category).all()

print("Category distribution:")
for cat, count in categories:
    print(f"  {cat}: {count}")

# Check urgency distribution
urgencies = session.query(
    Ticket.urgency,
    func.count(Ticket.id)
).group_by(Ticket.urgency).all()

print("Urgency distribution:")
for urgency, count in urgencies:
    print(f"  {urgency}: {count}")

# Check status distribution
statuses = session.query(
    Ticket.status,
    func.count(Ticket.id)
).group_by(Ticket.status).all()

print("Status distribution:")
for status, count in statuses:
    print(f"  {status}: {count}")

session.close()
```

---

## Rollback Plan

If migration fails:

### Immediate Rollback
```bash
# Stop new system
docker-compose down

# Restore old system
# Restore from backup or DNS failover

# Notify stakeholders
```

### Data Recovery
```bash
# If database corrupted
rm tickets.db

# Restore from backup
sqlite3 tickets.db < backup.sql

# Restart
docker-compose up -d
```

### Partial Rollback
```bash
# If some tickets corrupted
# Export good data
sqlite3 tickets.db "SELECT * FROM tickets WHERE id < 1000" > good_tickets.sql

# Delete corrupted
DELETE FROM tickets WHERE id >= 1000;

# Restore good data
sqlite3 tickets.db < good_tickets.sql
```

---

## Parallel Operation

If you want to run both systems temporarily:

### Load Balancer Setup
```nginx
upstream old_system {
    server old-system.internal:8000;
}

upstream new_system {
    server new-system.internal:8000;
}

server {
    listen 80;
    
    # Route 90% to new system, 10% to old
    location / {
        set $backend old_system;
        if ($cookie_use_new = "true") {
            set $backend new_system;
        }
        
        proxy_pass http://$backend;
    }
}
```

### Gradual Migration
1. Start with 10% of traffic to new system
2. Monitor error rates
3. Increase to 25%, 50%, 75%, 100%
4. Retire old system

---

## Training & Documentation

### User Guide
- [ ] Create screenshots of new UI
- [ ] Document key workflows
- [ ] Create video tutorials
- [ ] Provide quick reference cards
- [ ] Setup training sessions

### Admin Guide
- [ ] Document new system architecture
- [ ] Document backup procedures
- [ ] Document troubleshooting
- [ ] Document maintenance tasks
- [ ] Document escalation procedures

---

## Post-Migration Support

### First Week Monitoring
- [ ] Monitor error logs daily
- [ ] Check user feedback
- [ ] Verify performance metrics
- [ ] Review ticket quality
- [ ] Adjust AI classification if needed

### Issues Tracking
```python
# Monitor common issues
issues = [
    ("Incorrect classification", 0),
    ("Missing data", 0),
    ("Performance problems", 0),
    ("Permission issues", 0),
    ("API errors", 0)
]

# Track and report
```

### Optimization
- [ ] Tune database indices
- [ ] Adjust classification rules
- [ ] Update team assignments
- [ ] Optimize queries
- [ ] Cache frequently accessed data

---

## Success Metrics

- [ ] 100% data migrated
- [ ] <0.1% data loss
- [ ] <1 second response times
- [ ] <0.1% error rate
- [ ] 95%+ user satisfaction
- [ ] All workflows functional
- [ ] No data corruption
- [ ] Successful backups
- [ ] Team trained
- [ ] Documentation complete

---

**Migration Complete When:**
✅ All data migrated  
✅ Data validation passed  
✅ Users trained  
✅ Old system decommissioned  
✅ Support procedures established  
✅ Monitoring in place

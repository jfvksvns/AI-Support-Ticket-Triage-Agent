# 🆘 Troubleshooting FAQ

## Backend Issues

### Python & Environment

#### Q: ModuleNotFoundError: No module named 'fastapi'
**A:** Your virtual environment isn't activated or dependencies aren't installed.

```bash
# Activate virtual environment
cd backend
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Q: Python version mismatch
**A:** Ensure you have Python 3.11 or higher.

```bash
# Check version
python3 --version

# If needed, install correct version
# macOS:
brew install python@3.11

# Linux:
sudo apt-get install python3.11

# Windows: Download from python.org
```

#### Q: Permission denied when running python
**A:** Use `python3` explicitly or update PATH.

```bash
# Use explicit version
python3 main.py

# Or verify Python in PATH
which python3
```

---

### Database Issues

#### Q: Database error: "no such table: tickets"
**A:** Database hasn't been initialized.

```bash
# Initialize database
cd backend
python scripts/init_db.py

# Verify tables created
sqlite3 tickets.db ".tables"
```

#### Q: Database locked
**A:** SQLite database lock from previous crash.

```bash
# Remove lock files
rm backend/*.db-journal
rm backend/*.db-wal

# Restart server
python backend/main.py
```

#### Q: Database corruption
**A:** Restore from backup or reinitialize.

```bash
# Backup corrupted database
mv tickets.db tickets.db.corrupt

# Recreate
python scripts/init_db.py

# Restore data if available
# sqlite3 tickets.db < backup.sql
```

#### Q: SQLite too slow in production
**A:** SQLite not recommended for production. Use PostgreSQL.

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
createdb ticket_triage

# Update .env
DATABASE_URL=postgresql://user:password@localhost/ticket_triage

# Reinstall dependencies
pip install psycopg2-binary
```

---

### API Issues

#### Q: API not responding on port 8000
**A:** Port already in use or server crashed.

```bash
# Find process on port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
PORT=8001 python main.py

# Check if server started
curl http://localhost:8000/api/health
```

#### Q: 403 Forbidden error
**A:** API authentication enabled but key missing or wrong.

```bash
# Check if API_KEY is set
cat backend/.env | grep API_KEY

# Remove requirement in .env or provide key
# X-API-Key: your-key-here
curl -H "X-API-Key: your-key-here" http://localhost:8000/api/tickets
```

#### Q: CORS errors in browser console
**A:** Frontend and backend on different origins.

```bash
# Check backend CORS config
cat backend/app/main.py | grep "CORS"

# Update frontend URL in .env
VITE_API_URL=http://localhost:8000

# Verify API running on correct port
curl http://localhost:8000/api/health
```

#### Q: 500 Internal Server Error
**A:** Backend crashed or unhandled exception.

```bash
# Check logs
docker logs ticket-triage-backend  # if using Docker

# Or check console output
# Restart backend
python backend/main.py

# Check .env for missing variables
cat backend/.env | grep CLAUDE_API_KEY
```

---

### Claude API Issues

#### Q: Claude API error: "Invalid API Key"
**A:** API key missing, incorrect, or expired.

```bash
# Verify .env has correct key
cat backend/.env | grep CLAUDE_API_KEY

# Key should start with 'sk-ant-'
# Get new key from: https://console.anthropic.com/account/keys

# Update .env
nano backend/.env
# Set CLAUDE_API_KEY=sk-ant-your-real-key

# Restart backend
python backend/main.py
```

#### Q: Claude API timeout
**A:** Slow API response or network issue.

```bash
# Check Claude status
# https://status.anthropic.com/

# Increase timeout in .env
CLAUDE_TIMEOUT=60

# Check internet connection
ping api.anthropic.com

# Restart backend
python backend/main.py
```

#### Q: Claude API rate limit exceeded
**A:** Too many requests. Implement rate limiting.

```bash
# Check rate limits in API response headers
curl -v http://localhost:8000/api/classify

# Add request queuing
# Or upgrade API tier
```

---

## Frontend Issues

### Node & NPM

#### Q: npm command not found
**A:** Node.js not installed or not in PATH.

```bash
# Check version
node --version
npm --version

# If not found, install Node.js
# https://nodejs.org/

# macOS:
brew install node

# Linux:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Q: "node_modules" directory too large
**A:** Cache issue. Reinstall.

```bash
# Remove and reinstall
rm -rf node_modules package-lock.json
npm install

# Use npm ci for production
npm ci
```

---

### Development Server

#### Q: Port 5173 already in use
**A:** Another process using the port.

```bash
# Use different port
npm run dev -- --port 3001

# Or kill process on 5173
lsof -i :5173
kill -9 <PID>
```

#### Q: Frontend not connecting to backend
**A:** API URL misconfigured.

```bash
# Check .env
cat frontend/.env

# Should have:
VITE_API_URL=http://localhost:8000

# Verify backend running
curl http://localhost:8000/api/health

# Update if backend on different port
VITE_API_URL=http://localhost:8001
```

#### Q: Hot reload not working
**A:** Vite configuration issue.

```bash
# Check vite.config.ts
# Ensure HMR configured for your host/port

# Restart dev server
npm run dev

# Clear Vite cache
rm -rf node_modules/.vite
```

---

### Build Issues

#### Q: npm run build fails
**A:** TypeScript errors or missing dependencies.

```bash
# Type check
npm run type-check

# List errors
npm run build 2>&1 | head -50

# Install missing dependencies
npm install

# Try building again
npm run build
```

#### Q: Build output too large
**A:** Unoptimized bundle.

```bash
# Analyze bundle
npm install -D webpack-bundle-analyzer

# Check what's included
npm run build

# Remove unused dependencies
npm prune --production
```

---

### Dark Mode Issues

#### Q: Dark mode not toggling
**A:** CSS classes or localStorage not syncing.

```bash
# Check browser console
# Look for any CSS errors

# Clear localStorage
localStorage.clear()

# Refresh page
# Click dark mode toggle

# Check if 'dark' class applied to html
document.documentElement.classList
```

#### Q: Dark mode not persisting
**A:** localStorage not working or permissions issue.

```javascript
// Test localStorage in console
localStorage.setItem('test', 'value')
localStorage.getItem('test')

// Clear and reset
localStorage.clear()
location.reload()
```

---

## Docker Issues

### Docker Setup

#### Q: Docker daemon not running
**A:** Start Docker service.

```bash
# macOS (Docker Desktop)
open /Applications/Docker.app

# Linux
sudo systemctl start docker

# Verify running
docker ps
```

#### Q: Permission denied: /var/run/docker.sock
**A:** User not in docker group.

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Try again
docker ps
```

---

### Docker Compose

#### Q: docker-compose: command not found
**A:** Docker Compose not installed.

```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
```

#### Q: Container won't start
**A:** Check logs for errors.

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Check exit code
docker-compose ps

# Rebuild without cache
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### Q: CLAUDE_API_KEY not set
**A:** Environment variable not passed.

```bash
# Set before running
export CLAUDE_API_KEY="sk-ant-your-key"

# Or add to .env file
echo "CLAUDE_API_KEY=sk-ant-your-key" >> .env

# Then run
docker-compose up -d
```

#### Q: Containers using old code
**A:** Image cache issue.

```bash
# Rebuild images
docker-compose build --no-cache

# Or remove and recreate
docker-compose down
docker-compose up -d --build
```

---

## Integration Issues

### Frontend-Backend Connection

#### Q: CORS error: "No 'Access-Control-Allow-Origin' header"
**A:** CORS not configured correctly.

```bash
# Check backend CORS settings
cat backend/app/main.py | grep -A5 "CORSMiddleware"

# Should allow frontend origin
allow_origins=["http://localhost:5173", "http://localhost:3000"]

# Restart backend
python backend/main.py
```

#### Q: Ticket creation works but doesn't appear in list
**A:** Different databases or caching issue.

```bash
# Check database path
cat backend/.env | grep DATABASE_URL

# Both services should use same database
# Clear cache if applicable

# Restart both services
```

#### Q: API returns 404 for existing endpoint
**A:** Frontend using wrong API URL.

```bash
# Check frontend API URL
cat frontend/.env | grep VITE_API_URL

# Should match backend
VITE_API_URL=http://localhost:8000

# Check backend routes
curl http://localhost:8000/api/tickets

# If 404, check backend started correctly
python backend/main.py
```

---

## Performance Issues

#### Q: API slow to respond
**A:** Check backend performance.

```bash
# Monitor resources
docker stats

# Check database queries
# Enable query logging in SQLAlchemy

# Monitor backend logs
docker logs -f ticket-triage-backend

# Test endpoint speed
time curl http://localhost:8000/api/tickets
```

#### Q: Frontend sluggish
**A:** Check browser performance.

```bash
# Open DevTools (F12)
# Performance tab: record interaction
# Look for long tasks
# Check network tab for slow requests

# Monitor memory
# Look for memory leaks in React components
```

#### Q: Database queries slow
**A:** Missing indices or inefficient queries.

```bash
# Analyze query
sqlite3 tickets.db "EXPLAIN QUERY PLAN SELECT * FROM tickets WHERE urgency='Critical';"

# Add missing indices
sqlite3 tickets.db "CREATE INDEX IF NOT EXISTS idx_urgency ON tickets(urgency);"

# Check existing indices
sqlite3 tickets.db ".indices"
```

---

## Testing Issues

#### Q: Tests fail with database errors
**A:** Test database not isolated.

```bash
# Clear database
rm backend/tickets.db

# Run tests
pytest tests/ -v

# If issue persists, check conftest.py
cat backend/tests/conftest.py
```

#### Q: Tests hang or timeout
**A:** Waiting for external resource.

```bash
# Run with timeout
pytest tests/ --timeout=30 -v

# Check for infinite loops
# Kill hanging process
pkill -f pytest
```

#### Q: Import errors in tests
**A:** Path issues.

```bash
# Add backend to path
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"

# Or run from backend directory
cd backend && pytest tests/ -v
```

---

## Monitoring & Logs

#### Q: Can't find application logs
**A:** Check Docker or file system.

```bash
# Docker logs
docker logs ticket-triage-backend

# File logs (if configured)
tail -f backend/app.log

# System logs (if running as service)
journalctl -u ticket-triage-backend -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

#### Q: Logs getting too large
**A:** Implement log rotation.

```bash
# For Docker
# Add logging driver to docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

# For file logs
# Use logrotate utility
sudo tee /etc/logrotate.d/ticket-triage > /dev/null <<EOF
/path/to/app.log {
    daily
    rotate 7
    compress
    delaycompress
}
EOF
```

---

## Getting Help

### If You're Stuck

1. **Check Documentation**
   - README.md - Project overview
   - SETUP_GUIDE.md - Installation help
   - API docs at /api/docs
   - Code comments

2. **Check Logs**
   - Backend logs (stdout or file)
   - Frontend console (DevTools)
   - Docker logs
   - System logs

3. **Test Isolation**
   - Test backend with curl
   - Test frontend in browser
   - Test database directly
   - Test Docker independently

4. **Search GitHub Issues**
   - Look for similar issues
   - Check closed issues
   - Review pull requests

5. **Create Minimal Reproduction**
   - Share exact error message
   - Provide steps to reproduce
   - Include environment info
   - Provide logs

---

## Support Resources

- **Documentation**: /README.md, /SETUP_GUIDE.md
- **API Docs**: http://localhost:8000/api/docs
- **Code Examples**: Tests in backend/tests/
- **Issue Tracking**: GitHub Issues
- **Discussions**: GitHub Discussions

---

**Last Updated**: August 7, 2026  
**Version**: 1.0.0  
**Status**: Comprehensive FAQ Ready

# 🚀 Production Deployment Checklist

## Pre-Deployment Phase

### Planning
- [ ] Define infrastructure requirements
- [ ] Plan scaling strategy
- [ ] Determine backup strategy
- [ ] Plan monitoring approach
- [ ] Document runbooks
- [ ] Plan disaster recovery

### Security Review
- [ ] Review environment variables
- [ ] Audit API authentication
- [ ] Check input validation
- [ ] Review error messages
- [ ] Verify CORS configuration
- [ ] Check database permissions
- [ ] Review Docker configurations
- [ ] Scan dependencies for vulnerabilities

### Performance Testing
- [ ] Load test API (1000+ requests/min)
- [ ] Test database query performance
- [ ] Verify pagination on large datasets
- [ ] Test memory usage under load
- [ ] Check response times (<1s P95)
- [ ] Verify concurrent connection handling

### Documentation Review
- [ ] Verify README is accurate
- [ ] Check SETUP_GUIDE instructions
- [ ] Confirm API documentation
- [ ] Review deployment guide
- [ ] Document any custom configurations
- [ ] Create operations guide

---

## Infrastructure Setup

### AWS EC2 Deployment

#### Step 1: Instance Setup
- [ ] Launch EC2 instance (Ubuntu 22.04 LTS)
- [ ] Instance type: t3.large or larger
- [ ] Enable detailed monitoring
- [ ] Attach EBS volume for database
- [ ] Configure security group
  - [ ] Allow 80 (HTTP)
  - [ ] Allow 443 (HTTPS)
  - [ ] Allow 22 (SSH, restricted IP)
- [ ] Create and download key pair

#### Step 2: System Configuration
- [ ] SSH into instance
- [ ] Update system packages
  ```bash
  sudo apt-get update && sudo apt-get upgrade -y
  ```
- [ ] Install Docker
- [ ] Install Docker Compose
- [ ] Install nginx (for reverse proxy)
- [ ] Install certbot (for SSL)

#### Step 3: Application Setup
- [ ] Clone repository
- [ ] Create production .env file
- [ ] Set secure secrets
- [ ] Configure database location
- [ ] Build Docker images
- [ ] Test Docker Compose locally

#### Step 4: Database Setup
- [ ] Choose database (SQLite or PostgreSQL)
- [ ] If PostgreSQL:
  - [ ] Install PostgreSQL
  - [ ] Create database
  - [ ] Create database user with permissions
  - [ ] Configure backups
- [ ] Initialize schema
- [ ] Verify database connection

### Alternative: Heroku Deployment

- [ ] Create Heroku app
- [ ] Set environment variables
- [ ] Add Procfile
- [ ] Configure PostgreSQL add-on
- [ ] Deploy via git push
- [ ] Verify logs

### Alternative: Docker Swarm/Kubernetes

- [ ] Setup orchestration cluster
- [ ] Create persistent volumes
- [ ] Deploy services
- [ ] Configure networking
- [ ] Setup health checks
- [ ] Configure auto-scaling

---

## Configuration Checklist

### Environment Variables
- [ ] CLAUDE_API_KEY (secure, not in code)
- [ ] DATABASE_URL (production database)
- [ ] DEBUG = False
- [ ] LOG_LEVEL = INFO
- [ ] ENABLE_CORS = True (with allowed origins)
- [ ] API_KEY (if using API authentication)
- [ ] APP_NAME = "AI Support Ticket Triage"
- [ ] HOST = 0.0.0.0
- [ ] PORT = 8000 (or internal port)

### Database Configuration
- [ ] Database size: 100GB+ disk space
- [ ] Backup strategy: Daily backups
- [ ] Retention: 30-day backup retention
- [ ] Replication: Enable if available
- [ ] Monitoring: Database performance monitoring

### Application Configuration
- [ ] Python version: 3.11+
- [ ] Node version: 18+
- [ ] gunicorn workers: (CPU cores × 2) + 1
- [ ] Max database connections: 20-50
- [ ] Request timeout: 30 seconds
- [ ] Session timeout: 24 hours

### Reverse Proxy (Nginx)
- [ ] Configure upstream backends
- [ ] Setup SSL certificates
- [ ] Configure gzip compression
- [ ] Enable caching headers
- [ ] Setup logging
- [ ] Configure rate limiting

---

## Deployment Steps

### Step 1: Pre-Deployment Tests
```bash
# Backend tests
cd backend
pytest tests/ -v
# Verify all pass

# Frontend build
cd ../frontend
npm run build
# Verify no errors

# Docker build
docker-compose build
# Verify both images build successfully
```
- [ ] All backend tests pass
- [ ] Frontend builds successfully
- [ ] Docker images build
- [ ] No build warnings

### Step 2: Database Migration
```bash
# Initialize production database
python backend/scripts/init_db.py

# Verify tables created
sqlite3 backend/tickets.db ".tables"
```
- [ ] Database initialized
- [ ] Tables verified
- [ ] Indices created
- [ ] Schema validated

### Step 3: Environment Setup
```bash
# Create production .env
cp backend/.env.example backend/.env
nano backend/.env

# Set all required variables
# Verify sensitive data not in code
```
- [ ] CLAUDE_API_KEY set
- [ ] DATABASE_URL configured
- [ ] Security settings correct
- [ ] All required vars set

### Step 4: Docker Deployment
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Verify running
docker-compose ps

# Check logs
docker-compose logs -f
```
- [ ] Backend container running
- [ ] Frontend container running
- [ ] Health checks passing
- [ ] No startup errors

### Step 5: Health Checks
```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend accessibility
curl http://localhost:3000

# API accessibility
curl http://localhost:8000/api/docs
```
- [ ] Backend responding
- [ ] Frontend accessible
- [ ] API documentation available
- [ ] No 500 errors

### Step 6: SSL Certificate Setup
```bash
# Get certificate with Let's Encrypt
sudo certbot --nginx -d yourdomain.com

# Verify auto-renewal
sudo certbot renew --dry-run
```
- [ ] SSL certificate obtained
- [ ] Certificate auto-renewal configured
- [ ] HTTPS working
- [ ] Redirects from HTTP to HTTPS

### Step 7: Reverse Proxy Setup
```bash
# Configure nginx
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
# nginx config here
EOF

# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```
- [ ] Nginx configured
- [ ] Upstream backends correct
- [ ] SSL configured
- [ ] Proxying working

---

## Post-Deployment Validation

### Functionality Tests
```bash
# Create test ticket
curl -X POST https://yourdomain.com/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Ticket",
    "description": "Testing production deployment",
    "reporter_name": "Admin",
    "reporter_email": "admin@example.com",
    "department": "IT"
  }'

# List tickets
curl https://yourdomain.com/api/tickets

# Get statistics
curl https://yourdomain.com/api/statistics
```
- [ ] Can create tickets
- [ ] Can list tickets
- [ ] Can get statistics
- [ ] No errors in responses

### Performance Validation
```bash
# Load test
ab -n 1000 -c 10 https://yourdomain.com/api/health

# Check response times
for i in {1..10}; do
  curl -w "Time: %{time_total}s\n" \
    https://yourdomain.com/api/tickets
done
```
- [ ] Response time <1 second
- [ ] No 500 errors under load
- [ ] Memory stable
- [ ] CPU usage reasonable

### Security Validation
```bash
# Check SSL
curl -I https://yourdomain.com

# Verify CORS headers
curl -H "Origin: http://example.com" \
  -H "Access-Control-Request-Method: POST" \
  https://yourdomain.com/api/tickets -v
```
- [ ] HTTPS working
- [ ] Security headers present
- [ ] CORS configured correctly
- [ ] No sensitive data in headers

### Monitoring Setup
- [ ] Application monitoring (e.g., New Relic, Datadog)
- [ ] Database monitoring
- [ ] Log aggregation (e.g., ELK, Papertrail)
- [ ] Error tracking (e.g., Sentry)
- [ ] Uptime monitoring
- [ ] Performance monitoring

---

## Backup & Recovery

### Backup Strategy
- [ ] Automated daily backups
- [ ] 30-day backup retention
- [ ] Backup encryption enabled
- [ ] Backup testing (monthly)
- [ ] Restore procedures documented

### Backup Verification
```bash
# Backup database
docker exec ticket-triage-backend \
  sqlite3 /app/tickets.db ".backup '/backup/tickets.db.backup'"

# Verify backup
sqlite3 /backup/tickets.db.backup ".tables"
```
- [ ] Backup created successfully
- [ ] Backup can be restored
- [ ] Data integrity verified

### Disaster Recovery
- [ ] RTO (Recovery Time Objective) documented
- [ ] RPO (Recovery Point Objective) defined
- [ ] Failover procedures documented
- [ ] Disaster recovery drills scheduled

---

## Monitoring & Maintenance

### Monitoring Setup
- [ ] Application health checks (every 60 seconds)
- [ ] Database monitoring
- [ ] Disk space monitoring (alert at 80%)
- [ ] Memory monitoring (alert at 85%)
- [ ] CPU monitoring (alert at 90%)
- [ ] Error rate monitoring (alert at >1%)
- [ ] Response time monitoring (alert at >2s)

### Log Configuration
```bash
# Application logs
docker logs ticket-triage-backend

# Error logs
docker logs ticket-triage-backend --tail 100 | grep ERROR

# Request logs
docker logs ticket-triage-backend | grep "POST\|GET\|PATCH\|DELETE"
```
- [ ] Application logs captured
- [ ] Error logs monitored
- [ ] Log retention configured
- [ ] Log alerts configured

### Regular Maintenance
- [ ] Weekly log review
- [ ] Monthly security updates
- [ ] Quarterly database optimization
- [ ] Annual capacity planning
- [ ] Document changes in runbook

---

## Scaling Checklist

### Horizontal Scaling
- [ ] Load balancer configured
- [ ] Multiple backend instances
- [ ] Session sharing (if needed)
- [ ] Database connection pooling
- [ ] Cache layer (Redis, optional)

### Vertical Scaling
- [ ] Increase instance size
- [ ] Increase database resources
- [ ] Increase memory allocation
- [ ] Monitor resource utilization

### Database Scaling
- [ ] Index optimization
- [ ] Query optimization
- [ ] Connection pooling
- [ ] Read replicas (if needed)
- [ ] Sharding (if needed)

---

## Security Hardening

### Application Security
- [ ] Environment variables for secrets
- [ ] API authentication enabled
- [ ] Input validation enabled
- [ ] Output encoding enabled
- [ ] SQL injection prevention
- [ ] CSRF protection enabled
- [ ] Rate limiting enabled
- [ ] CORS properly configured

### Infrastructure Security
- [ ] SSL/TLS certificates current
- [ ] Security group restrictions
- [ ] SSH key management
- [ ] Firewall rules
- [ ] VPN for admin access
- [ ] DDoS protection (optional)
- [ ] WAF rules (optional)

### Data Security
- [ ] Database encryption at rest
- [ ] Database encryption in transit
- [ ] Backup encryption
- [ ] Access controls
- [ ] Data retention policies
- [ ] Data deletion procedures

---

## Post-Launch Monitoring

### First 24 Hours
- [ ] Monitor error rates (target: <0.1%)
- [ ] Monitor response times (target: <1s)
- [ ] Monitor resource usage
- [ ] Check user feedback
- [ ] Monitor database size growth

### First Week
- [ ] Performance baseline established
- [ ] Scaling needs identified
- [ ] Monitoring alerts tuned
- [ ] Incident procedures tested
- [ ] Team trained on runbooks

### Ongoing
- [ ] Daily log review
- [ ] Weekly metrics review
- [ ] Monthly security updates
- [ ] Quarterly capacity planning
- [ ] Annual architecture review

---

## Deployment Sign-Off

### Technical Lead
- [ ] Deployment plan reviewed
- [ ] Architecture approved
- [ ] Security audit passed
- [ ] Performance baseline set
- [ ] Monitoring configured

### Operations Team
- [ ] Runbooks documented
- [ ] On-call procedures established
- [ ] Escalation paths defined
- [ ] Monitoring set up
- [ ] Alert thresholds calibrated

### Management
- [ ] Business requirements met
- [ ] SLA targets achievable
- [ ] Budget approved
- [ ] Timeline acceptable
- [ ] Risk assessment completed

---

## Rollback Plan

### If Issues Occur
1. Identify issue severity
2. Trigger incident response
3. Decide on rollback vs. hotfix
4. If rollback:
   - Stop new service
   - Restore from backup
   - Verify restoration
   - Resume old service
5. Conduct post-mortem
6. Document lessons learned

### Rollback Commands
```bash
# Stop new deployment
docker-compose down

# Restore previous version
git revert HEAD

# Restore database backup
docker cp /backup/tickets.db.backup $(docker-compose ps -q backend):/app/tickets.db

# Start services
docker-compose up -d

# Verify health
curl https://yourdomain.com/api/health
```

---

## Success Criteria

- [ ] All systems operational
- [ ] Health checks passing
- [ ] Response times < 1 second
- [ ] Error rate < 0.1%
- [ ] Database stable
- [ ] Backups working
- [ ] Monitoring alerting
- [ ] Team trained
- [ ] Documentation complete
- [ ] Support procedures in place

---

**Deployment Status**: Ready for Production  
**Last Updated**: August 7, 2026  
**Version**: 1.0.0

"""
Generate sample ticket data for testing and demonstration.
Creates 30 diverse tickets across all categories with various statuses and urgencies.

Usage:
    python scripts/generate_sample_data.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
import random

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.database import Ticket, Base
from app.database.engine import DatabaseEngine


SAMPLE_TICKETS = [
    {
        "subject": "Cannot connect to VPN",
        "description": "I've been unable to connect to the company VPN for the past 2 hours. I've tried restarting my machine and the VPN client, but still getting connection errors. The error code is 0x800704CF.",
        "reporter_name": "John Doe",
        "reporter_email": "john.doe@company.com",
        "department": "Sales",
        "category": "Network",
        "urgency": "High",
        "confidence": 92,
        "assigned_team": "Network Team",
    },
    {
        "subject": "Laptop won't start after update",
        "description": "My laptop freezes during the Windows update and won't boot. I see a blue screen with error code 0xC000021A. Need urgent assistance as I have a client meeting in 1 hour.",
        "reporter_name": "Sarah Smith",
        "reporter_email": "sarah.smith@company.com",
        "department": "Marketing",
        "category": "Hardware",
        "urgency": "Critical",
        "confidence": 88,
        "assigned_team": "IT Support",
    },
    {
        "subject": "Email not syncing on mobile",
        "description": "Outlook on my iPhone stopped syncing emails. Last sync was yesterday at 3 PM. Other apps are working fine. I've tried removing and re-adding the account.",
        "reporter_name": "Mike Johnson",
        "reporter_email": "mike.johnson@company.com",
        "department": "Finance",
        "category": "Email",
        "urgency": "Medium",
        "confidence": 79,
        "assigned_team": "Service Desk",
    },
    {
        "subject": "Printer jamming constantly",
        "description": "The HP LaserJet in the 3rd floor break room keeps jamming. Error code 13.10 on the display. It's jammed right now and blocking everyone's print jobs.",
        "reporter_name": "Lisa Wong",
        "reporter_email": "lisa.wong@company.com",
        "department": "HR",
        "category": "Printer",
        "urgency": "Medium",
        "confidence": 95,
        "assigned_team": "IT Support",
    },
    {
        "subject": "Database query timeout",
        "description": "Our nightly ETL process is timing out. Query takes 45 minutes now instead of 5. The database server shows high CPU usage. Need performance analysis.",
        "reporter_name": "Alex Kumar",
        "reporter_email": "alex.kumar@company.com",
        "department": "Engineering",
        "category": "Database",
        "urgency": "Critical",
        "confidence": 85,
        "assigned_team": "Database Team",
    },
    {
        "subject": "Need password reset",
        "description": "I forgot my Active Directory password. I can't log into my computer or email. Please reset it to my temporary password.",
        "reporter_name": "Tom Brown",
        "reporter_email": "tom.brown@company.com",
        "department": "Operations",
        "category": "Access Management",
        "urgency": "High",
        "confidence": 97,
        "assigned_team": "Security Team",
    },
    {
        "subject": "AWS CloudFront distribution error",
        "description": "Our CDN is returning 503 Service Unavailable errors. Traffic is being affected. CloudWatch shows spike in origin errors. Need immediate investigation.",
        "reporter_name": "Emma Davis",
        "reporter_email": "emma.davis@company.com",
        "department": "Infrastructure",
        "category": "Cloud",
        "urgency": "Critical",
        "confidence": 88,
        "assigned_team": "Cloud Team",
    },
    {
        "subject": "Software license issue",
        "description": "Adobe Creative Suite license expired and I can't renew it. Getting license error when opening Photoshop. Blocking my design work.",
        "reporter_name": "Jessica Lee",
        "reporter_email": "jessica.lee@company.com",
        "department": "Design",
        "category": "Software",
        "urgency": "High",
        "confidence": 81,
        "assigned_team": "Application Team",
    },
    {
        "subject": "Suspected malware infection",
        "description": "My computer is slow and running strange processes. I see pop-ups appearing randomly. Antivirus is showing suspicious activity. Please scan and advise.",
        "reporter_name": "Robert Chen",
        "reporter_email": "robert.chen@company.com",
        "department": "Executive",
        "category": "Security",
        "urgency": "Critical",
        "confidence": 76,
        "assigned_team": "Security Team",
    },
    {
        "subject": "Slow internet connection",
        "description": "My internet speed is extremely slow. Speedtest shows 1Mbps down when it should be 100Mbps. Video calls are lagging.",
        "reporter_name": "Patricia Moore",
        "reporter_email": "patricia.moore@company.com",
        "department": "Legal",
        "category": "Network",
        "urgency": "Medium",
        "confidence": 82,
        "assigned_team": "Network Team",
    },
    {
        "subject": "Cannot access shared drive",
        "description": "I'm getting permission denied error when trying to access the Sales shared drive. I used to have access but lost it after yesterday's system changes.",
        "reporter_name": "Kevin White",
        "reporter_email": "kevin.white@company.com",
        "department": "Sales",
        "category": "Access Management",
        "urgency": "High",
        "confidence": 91,
        "assigned_team": "Security Team",
    },
    {
        "subject": "Application crash on startup",
        "description": "Custom CRM application crashes immediately after launching. Error code: Exception_Access_Violation. Tried reinstalling but same issue. Blocks work.",
        "reporter_name": "Susan Martinez",
        "reporter_email": "susan.martinez@company.com",
        "department": "Customer Service",
        "category": "Software",
        "urgency": "Critical",
        "confidence": 87,
        "assigned_team": "Application Team",
    },
    {
        "subject": "Need multi-monitor setup",
        "description": "Just got assigned to new role. Need second monitor for my workstation. Also need new USB-C dock.",
        "reporter_name": "Daniel Lee",
        "reporter_email": "daniel.lee@company.com",
        "department": "Engineering",
        "category": "Hardware",
        "urgency": "Low",
        "confidence": 89,
        "assigned_team": "IT Support",
    },
    {
        "subject": "Cannot access Azure Portal",
        "description": "Azure Portal login fails with 'invalid credentials'. I'm using correct credentials. Other cloud services work fine.",
        "reporter_name": "Angela Davis",
        "reporter_email": "angela.davis@company.com",
        "department": "Cloud",
        "category": "Cloud",
        "urgency": "High",
        "confidence": 84,
        "assigned_team": "Cloud Team",
    },
    {
        "subject": "Backup job failed overnight",
        "description": "Database backup failed with 'insufficient disk space' error. Need to clear space urgently before next scheduled backup.",
        "reporter_name": "Michael Rodriguez",
        "reporter_email": "michael.rodriguez@company.com",
        "department": "IT",
        "category": "Database",
        "urgency": "Critical",
        "confidence": 93,
        "assigned_team": "Database Team",
    },
    {
        "subject": "Outlook meeting sync issue",
        "description": "Calendar meetings not syncing across devices. Mobile shows different meetings than desktop. This is causing scheduling conflicts.",
        "reporter_name": "Rachel Green",
        "reporter_email": "rachel.green@company.com",
        "department": "Project Management",
        "category": "Email",
        "urgency": "Medium",
        "confidence": 75,
        "assigned_team": "Service Desk",
    },
    {
        "subject": "SSL certificate expired",
        "description": "Internal website showing SSL certificate error. Certificate expired yesterday. Browsers are blocking access. Need immediate renewal.",
        "reporter_name": "James Wilson",
        "reporter_email": "james.wilson@company.com",
        "department": "Infrastructure",
        "category": "Security",
        "urgency": "Critical",
        "confidence": 96,
        "assigned_team": "Security Team",
    },
    {
        "subject": "Monitor flickering",
        "description": "My Dell monitor keeps flickering on and off. Started this morning. Makes it hard to work. Tried different cable but same issue.",
        "reporter_name": "Donna Harris",
        "reporter_email": "donna.harris@company.com",
        "department": "Accounting",
        "category": "Hardware",
        "urgency": "Low",
        "confidence": 88,
        "assigned_team": "IT Support",
    },
    {
        "subject": "API rate limiting issue",
        "description": "Our API client is getting 429 rate limit errors. We just hit production scale. Need to increase rate limits.",
        "reporter_name": "Chris Anderson",
        "reporter_email": "chris.anderson@company.com",
        "department": "Engineering",
        "category": "Software",
        "urgency": "High",
        "confidence": 80,
        "assigned_team": "Application Team",
    },
    {
        "subject": "Network latency high",
        "description": "Ping to headquarters is 200ms, normally 20ms. VoIP calls have delays. Trace route shows packet loss at ISP level.",
        "reporter_name": "Brian Taylor",
        "reporter_email": "brian.taylor@company.com",
        "department": "Remote Office",
        "category": "Network",
        "urgency": "High",
        "confidence": 85,
        "assigned_team": "Network Team",
    },
    {
        "subject": "SQL injection vulnerability found",
        "description": "Security scan found SQL injection vulnerability in login form. Need urgent patch before going to production.",
        "reporter_name": "Lisa Anderson",
        "reporter_email": "lisa.anderson@company.com",
        "department": "Security",
        "category": "Security",
        "urgency": "Critical",
        "confidence": 98,
        "assigned_team": "Security Team",
    },
    {
        "subject": "Need new software license",
        "description": "Need to install Visual Studio Pro for new developer. Can someone help with licensing and installation?",
        "reporter_name": "David Park",
        "reporter_email": "david.park@company.com",
        "department": "Engineering",
        "category": "Software",
        "urgency": "Low",
        "confidence": 87,
        "assigned_team": "Application Team",
    },
    {
        "subject": "Kubernetes pod crashing",
        "description": "K8s pod keeps restarting. Logs show OOMKilled error. Memory limit needs to be increased. Affecting production service.",
        "reporter_name": "Nina Patel",
        "reporter_email": "nina.patel@company.com",
        "department": "DevOps",
        "category": "Cloud",
        "urgency": "Critical",
        "confidence": 89,
        "assigned_team": "Cloud Team",
    },
    {
        "subject": "Excel file corruption",
        "description": "Critical financial spreadsheet is corrupted and won't open. Error says file format is invalid. I have no recent backup.",
        "reporter_name": "George Garcia",
        "reporter_email": "george.garcia@company.com",
        "department": "Finance",
        "category": "Software",
        "urgency": "High",
        "confidence": 72,
        "assigned_team": "Application Team",
    },
    {
        "subject": "Firewall blocks legitimate traffic",
        "description": "Some legitimate API calls to vendor are being blocked by firewall. Need whitelist rules. Service is degraded.",
        "reporter_name": "Helen Martinez",
        "reporter_email": "helen.martinez@company.com",
        "department": "Security",
        "category": "Network",
        "urgency": "High",
        "confidence": 83,
        "assigned_team": "Network Team",
    },
    {
        "subject": "Slack integration not working",
        "description": "Slack bot integration stopped posting messages. Webhook errors appearing. Other integrations working fine.",
        "reporter_name": "Frank Lee",
        "reporter_email": "frank.lee@company.com",
        "department": "Engineering",
        "category": "Software",
        "urgency": "Medium",
        "confidence": 78,
        "assigned_team": "Application Team",
    },
    {
        "subject": "Storage quota exceeded",
        "description": "My OneDrive is full. Can't sync new files. Getting warning messages. Need quota increase.",
        "reporter_name": "Olivia Brown",
        "reporter_email": "olivia.brown@company.com",
        "department": "HR",
        "category": "Other",
        "urgency": "Low",
        "confidence": 90,
        "assigned_team": "Service Desk",
    },
    {
        "subject": "Docker registry authentication failed",
        "description": "CI/CD pipeline failing because Docker registry login is failing. Pipeline is blocked.",
        "reporter_name": "Peter Johnson",
        "reporter_email": "peter.johnson@company.com",
        "department": "DevOps",
        "category": "Software",
        "urgency": "High",
        "confidence": 86,
        "assigned_team": "Application Team",
    },
    {
        "subject": "DNS resolution issue",
        "description": "Internal DNS name resolution failing intermittently. Services are unreachable some of the time.",
        "reporter_name": "Rebecca Clark",
        "reporter_email": "rebecca.clark@company.com",
        "department": "Infrastructure",
        "category": "Network",
        "urgency": "High",
        "confidence": 84,
        "assigned_team": "Network Team",
    },
]

def generate_sample_data():
    """Generate and insert sample ticket data into the database."""
    try:
        # Initialize database
        DatabaseEngine.initialize()
        print("✓ Database initialized")

        # Create sample tickets
        session = DatabaseEngine.get_session()
        
        # Delete existing tickets
        session.query(Ticket).delete()
        session.commit()
        print("✓ Cleared existing tickets")

        # Insert sample tickets
        tickets = []
        base_date = datetime.now(timezone.utc) - timedelta(days=30)

        for i, ticket_data in enumerate(SAMPLE_TICKETS):
            # Vary creation dates over past 30 days
            created_at = base_date + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            # Vary status
            statuses = ["Open", "Assigned", "In Progress", "Pending Human Review", "Resolved", "Closed"]
            status = random.choice(statuses)

            # Randomly flag for human review if confidence < 75
            requires_review = ticket_data["confidence"] < 75 and random.random() > 0.5

            ticket = Ticket(
                subject=ticket_data["subject"],
                description=ticket_data["description"],
                reporter_name=ticket_data["reporter_name"],
                reporter_email=ticket_data["reporter_email"],
                department=ticket_data["department"],
                category=ticket_data["category"],
                urgency=ticket_data["urgency"],
                confidence=ticket_data["confidence"],
                assigned_team=ticket_data["assigned_team"],
                summary=f"{ticket_data['category']} issue - {ticket_data['urgency'].lower()} priority",
                reasoning=f"Classified as {ticket_data['category']} based on content analysis. Confidence: {ticket_data['confidence']}%",
                suggested_response=f"Thank you for reporting this {ticket_data['category'].lower()} issue. Our {ticket_data['assigned_team']} is now assigned and will work on this immediately.",
                status=status,
                requires_human_review=requires_review,
                created_at=created_at,
                updated_at=created_at + timedelta(hours=random.randint(0, 48))
            )
            tickets.append(ticket)

        session.add_all(tickets)
        session.commit()
        print(f"✓ Created {len(tickets)} sample tickets")

        # Print summary
        print("\n📊 Sample Data Summary:")
        print(f"   Total tickets: {len(tickets)}")
        print(f"   Categories: {len(set(t.category for t in tickets))}")
        print(f"   Statuses: {len(set(t.status for t in tickets))}")
        print(f"   Urgencies: {len(set(t.urgency for t in tickets))}")
        print(f"   Avg confidence: {sum(t.confidence for t in tickets) / len(tickets):.1f}%")
        print(f"   For review: {sum(1 for t in tickets if t.requires_human_review)}")

        session.close()
        print("\n✅ Sample data generation completed successfully!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    generate_sample_data()

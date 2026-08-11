"""
Analytics service for generating ticket statistics and dashboard metrics.
Provides data for analytics charts and summary cards.
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.database import Ticket
from app.models.schemas import StatisticsResponse
from app.core.constants import TicketUrgency, TicketCategory, AssignedTeam, TicketStatus

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for generating analytics and statistics from ticket data.
    
    Provides:
    - Ticket count aggregations
    - Distribution by category, urgency, team, status
    - Confidence metrics
    - Human review statistics
    - Time-based analytics
    """

    @staticmethod
    def get_statistics(db: Session) -> StatisticsResponse:
        """
        Generate comprehensive statistics for the dashboard.
        
        Args:
            db: Database session
            
        Returns:
            StatisticsResponse: Complete statistics object
        """
        try:
            total_tickets = db.query(Ticket).count()

            # Count by urgency
            critical_tickets = db.query(Ticket).filter(
                Ticket.urgency == TicketUrgency.CRITICAL.value
            ).count()
            high_tickets = db.query(Ticket).filter(
                Ticket.urgency == TicketUrgency.HIGH.value
            ).count()
            medium_tickets = db.query(Ticket).filter(
                Ticket.urgency == TicketUrgency.MEDIUM.value
            ).count()
            low_tickets = db.query(Ticket).filter(
                Ticket.urgency == TicketUrgency.LOW.value
            ).count()

            # Average confidence
            avg_confidence_result = db.query(func.avg(Ticket.confidence)).scalar()
            average_confidence = float(avg_confidence_result) if avg_confidence_result else 0.0

            # Human review count
            human_review_count = db.query(Ticket).filter(
                Ticket.requires_human_review == True
            ).count()

            # Distribution by category
            category_distribution = AnalyticsService._get_category_distribution(db)

            # Distribution by urgency
            urgency_distribution = AnalyticsService._get_urgency_distribution(db)

            # Distribution by team
            team_distribution = AnalyticsService._get_team_distribution(db)

            # Distribution by status
            status_distribution = AnalyticsService._get_status_distribution(db)

            return StatisticsResponse(
                total_tickets=total_tickets,
                critical_tickets=critical_tickets,
                high_tickets=high_tickets,
                medium_tickets=medium_tickets,
                low_tickets=low_tickets,
                average_confidence=round(average_confidence, 2),
                human_review_count=human_review_count,
                category_distribution=category_distribution,
                urgency_distribution=urgency_distribution,
                team_distribution=team_distribution,
                status_distribution=status_distribution
            )

        except Exception as e:
            logger.error(f"Error generating statistics: {str(e)}")
            # Return empty statistics on error
            return StatisticsResponse(
                total_tickets=0,
                critical_tickets=0,
                high_tickets=0,
                medium_tickets=0,
                low_tickets=0,
                average_confidence=0.0,
                human_review_count=0,
                category_distribution={},
                urgency_distribution={},
                team_distribution={},
                status_distribution={}
            )

    @staticmethod
    def _get_category_distribution(db: Session) -> Dict[str, int]:
        """
        Get ticket count by category.
        
        Args:
            db: Database session
            
        Returns:
            dict: Category names mapped to ticket counts
        """
        try:
            results = db.query(
                Ticket.category,
                func.count(Ticket.id).label("count")
            ).group_by(Ticket.category).all()

            return {category: count for category, count in results}

        except Exception as e:
            logger.error(f"Error getting category distribution: {str(e)}")
            return {}

    @staticmethod
    def _get_urgency_distribution(db: Session) -> Dict[str, int]:
        """
        Get ticket count by urgency level.
        
        Args:
            db: Database session
            
        Returns:
            dict: Urgency levels mapped to ticket counts
        """
        try:
            results = db.query(
                Ticket.urgency,
                func.count(Ticket.id).label("count")
            ).group_by(Ticket.urgency).all()

            distribution = {urgency: count for urgency, count in results}
            
            # Ensure all urgency levels are present (even if count is 0)
            for urgency in TicketUrgency.get_all_values():
                if urgency not in distribution:
                    distribution[urgency] = 0

            return distribution

        except Exception as e:
            logger.error(f"Error getting urgency distribution: {str(e)}")
            return {}

    @staticmethod
    def _get_team_distribution(db: Session) -> Dict[str, int]:
        """
        Get ticket count by assigned team.
        
        Args:
            db: Database session
            
        Returns:
            dict: Team names mapped to ticket counts
        """
        try:
            results = db.query(
                Ticket.assigned_team,
                func.count(Ticket.id).label("count")
            ).group_by(Ticket.assigned_team).all()

            distribution = {team: count for team, count in results}
            
            # Ensure all teams are present (even if count is 0)
            for team in AssignedTeam.get_all_values():
                if team not in distribution:
                    distribution[team] = 0

            return distribution

        except Exception as e:
            logger.error(f"Error getting team distribution: {str(e)}")
            return {}

    @staticmethod
    def _get_status_distribution(db: Session) -> Dict[str, int]:
        """
        Get ticket count by status.
        
        Args:
            db: Database session
            
        Returns:
            dict: Status values mapped to ticket counts
        """
        try:
            results = db.query(
                Ticket.status,
                func.count(Ticket.id).label("count")
            ).group_by(Ticket.status).all()

            distribution = {status: count for status, count in results}
            
            # Ensure all statuses are present (even if count is 0)
            for status in TicketStatus.get_all_values():
                if status not in distribution:
                    distribution[status] = 0

            return distribution

        except Exception as e:
            logger.error(f"Error getting status distribution: {str(e)}")
            return {}

    @staticmethod
    def get_tickets_per_day(
        db: Session,
        days: int = 30
    ) -> List[Dict]:
        """
        Get ticket creation count per day for the last N days.
        Useful for trend charts.
        
        Args:
            db: Database session
            days: Number of days to look back
            
        Returns:
            List[Dict]: List of {date, count} objects
        """
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

            results = db.query(
                func.date(Ticket.created_at).label("date"),
                func.count(Ticket.id).label("count")
            ).filter(
                Ticket.created_at >= cutoff_date
            ).group_by(
                func.date(Ticket.created_at)
            ).order_by(
                func.date(Ticket.created_at)
            ).all()

            return [{"date": str(date), "count": count} for date, count in results]

        except Exception as e:
            logger.error(f"Error getting tickets per day: {str(e)}")
            return []

    @staticmethod
    def get_average_confidence_by_category(db: Session) -> Dict[str, float]:
        """
        Get average AI confidence score by ticket category.
        
        Args:
            db: Database session
            
        Returns:
            dict: Category names mapped to average confidence scores
        """
        try:
            results = db.query(
                Ticket.category,
                func.avg(Ticket.confidence).label("avg_confidence")
            ).group_by(Ticket.category).all()

            return {
                category: round(float(avg_conf), 2)
                for category, avg_conf in results
                if avg_conf is not None
            }

        except Exception as e:
            logger.error(f"Error getting avg confidence by category: {str(e)}")
            return {}

    @staticmethod
    def get_team_workload(db: Session) -> Dict[str, Dict]:
        """
        Get current workload status for each team.
        
        Args:
            db: Database session
            
        Returns:
            dict: Team names mapped to workload info
        """
        try:
            workload = {}
            
            for team in AssignedTeam.get_all_values():
                total = db.query(Ticket).filter(
                    Ticket.assigned_team == team
                ).count()
                
                open_tickets = db.query(Ticket).filter(
                    Ticket.assigned_team == team,
                    Ticket.status.in_(["Open", "Assigned", "In Progress"])
                ).count()
                
                critical = db.query(Ticket).filter(
                    Ticket.assigned_team == team,
                    Ticket.urgency == TicketUrgency.CRITICAL.value
                ).count()

                workload[team] = {
                    "total": total,
                    "open": open_tickets,
                    "critical": critical
                }

            return workload

        except Exception as e:
            logger.error(f"Error getting team workload: {str(e)}")
            return {}

    @staticmethod
    def get_human_review_candidates(
        db: Session,
        limit: int = 10
    ) -> List[Ticket]:
        """
        Get tickets flagged for human review, sorted by priority.
        
        Args:
            db: Database session
            limit: Maximum number of tickets to return
            
        Returns:
            List[Ticket]: Tickets pending human review
        """
        try:
            tickets = db.query(Ticket).filter(
                Ticket.requires_human_review == True,
                Ticket.status != TicketStatus.RESOLVED.value,
                Ticket.status != TicketStatus.CLOSED.value
            ).order_by(
                # Priority order: Critical > High > Medium > Low
                Ticket.urgency.desc(),
                Ticket.created_at
            ).limit(limit).all()

            return tickets

        except Exception as e:
            logger.error(f"Error getting human review candidates: {str(e)}")
            return []

    @staticmethod
    def get_confidence_metrics(db: Session) -> Dict:
        """
        Get detailed confidence score metrics.
        
        Args:
            db: Database session
            
        Returns:
            dict: Confidence metrics including min, max, avg, stddev
        """
        try:
            from sqlalchemy import func as sqlalchemy_func

            results = db.query(
                sqlalchemy_func.count(Ticket.id).label("count"),
                sqlalchemy_func.avg(Ticket.confidence).label("avg"),
                sqlalchemy_func.min(Ticket.confidence).label("min"),
                sqlalchemy_func.max(Ticket.confidence).label("max")
            ).first()

            return {
                "total": results.count or 0,
                "average": round(float(results.avg), 2) if results.avg else 0.0,
                "minimum": results.min or 0,
                "maximum": results.max or 0
            }

        except Exception as e:
            logger.error(f"Error getting confidence metrics: {str(e)}")
            return {
                "total": 0,
                "average": 0.0,
                "minimum": 0,
                "maximum": 0
            }

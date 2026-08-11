"""
Unit tests for FastAPI route handlers.
Tests all API endpoints for correct behavior and error handling.
"""

import pytest
from fastapi import status


class TestClassifyEndpoint:
    """Tests for the /classify endpoint."""

    def test_classify_valid_ticket(self, client, sample_ticket_data):
        """Test classification of a valid ticket."""
        response = client.post(
            "/api/classify",
            json={
                "subject": sample_ticket_data["subject"],
                "description": sample_ticket_data["description"]
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "classification" in data
        classification = data["classification"]
        
        assert "category" in classification
        assert "urgency" in classification
        assert "confidence" in classification
        assert "assigned_team" in classification
        assert "summary" in classification
        assert "reasoning" in classification
        assert "suggested_response" in classification
        assert "requires_human_review" in classification

    def test_classify_missing_subject(self, client, sample_ticket_data):
        """Test classification fails with missing subject."""
        response = client.post(
            "/api/classify",
            json={
                "description": sample_ticket_data["description"]
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_classify_missing_description(self, client, sample_ticket_data):
        """Test classification fails with missing description."""
        response = client.post(
            "/api/classify",
            json={
                "subject": sample_ticket_data["subject"]
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_classify_short_subject(self, client):
        """Test classification fails with too-short subject."""
        response = client.post(
            "/api/classify",
            json={
                "subject": "VPN",
                "description": "I have a problem with VPN connectivity"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateTicketEndpoint:
    """Tests for the POST /tickets endpoint."""

    def test_create_ticket_success(self, client, sample_ticket_data):
        """Test successful ticket creation."""
        response = client.post(
            "/api/tickets",
            json=sample_ticket_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert "id" in data
        assert data["subject"] == sample_ticket_data["subject"]
        assert data["description"] == sample_ticket_data["description"]
        assert data["reporter_name"] == sample_ticket_data["reporter_name"]
        assert data["reporter_email"] == sample_ticket_data["reporter_email"]
        assert data["department"] == sample_ticket_data["department"]
        assert "category" in data
        assert "urgency" in data
        assert "assigned_team" in data

    def test_create_ticket_missing_field(self, client, sample_ticket_data):
        """Test ticket creation fails with missing field."""
        del sample_ticket_data["subject"]
        
        response = client.post(
            "/api/tickets",
            json=sample_ticket_data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_ticket_invalid_email(self, client, sample_ticket_data):
        """Test ticket creation fails with invalid email."""
        sample_ticket_data["reporter_email"] = "invalid-email"
        
        response = client.post(
            "/api/tickets",
            json=sample_ticket_data
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListTicketsEndpoint:
    """Tests for the GET /tickets endpoint."""

    def test_list_tickets_empty(self, client):
        """Test listing tickets when none exist."""
        response = client.get("/api/tickets")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["items"] == []
        assert data["total"] == 0
        assert data["skip"] == 0
        assert data["limit"] == 50

    def test_list_tickets_with_data(self, client, sample_ticket_data):
        """Test listing tickets with data."""
        # Create a ticket first
        client.post("/api/tickets", json=sample_ticket_data)
        
        # List tickets
        response = client.get("/api/tickets")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data["items"]) > 0
        assert data["total"] > 0

    def test_list_tickets_pagination(self, client, sample_ticket_data):
        """Test pagination parameters."""
        response = client.get(
            "/api/tickets",
            params={"skip": 0, "limit": 10}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["skip"] == 0
        assert data["limit"] == 10

    def test_list_tickets_filter_by_urgency(self, client, sample_ticket_data):
        """Test filtering by urgency."""
        # Create a ticket
        client.post("/api/tickets", json=sample_ticket_data)
        
        # Filter by urgency
        response = client.get(
            "/api/tickets",
            params={"urgency": "High"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # All returned items should have the specified urgency
        for item in data["items"]:
            assert item["urgency"] == "High"


class TestGetTicketEndpoint:
    """Tests for the GET /tickets/{ticket_id} endpoint."""

    def test_get_ticket_success(self, client, sample_ticket_data):
        """Test retrieving an existing ticket."""
        # Create a ticket
        create_response = client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_response.json()["id"]
        
        # Get the ticket
        response = client.get(f"/api/tickets/{ticket_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["id"] == ticket_id
        assert data["subject"] == sample_ticket_data["subject"]

    def test_get_ticket_not_found(self, client):
        """Test retrieving a non-existent ticket."""
        response = client.get("/api/tickets/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateTicketStatusEndpoint:
    """Tests for the PATCH /tickets/{ticket_id}/status endpoint."""

    def test_update_ticket_status(self, client, sample_ticket_data):
        """Test updating ticket status."""
        # Create a ticket
        create_response = client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_response.json()["id"]
        
        # Update status
        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            json={"status": "In Progress"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "In Progress"

    def test_update_ticket_status_invalid_status(self, client, sample_ticket_data):
        """Test updating with invalid status."""
        # Create a ticket
        create_response = client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_response.json()["id"]
        
        # Update with invalid status
        response = client.patch(
            f"/api/tickets/{ticket_id}/status",
            json={"status": "Invalid Status"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_ticket_status_not_found(self, client):
        """Test updating status of non-existent ticket."""
        response = client.patch(
            "/api/tickets/9999/status",
            json={"status": "Resolved"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteTicketEndpoint:
    """Tests for the DELETE /tickets/{ticket_id} endpoint."""

    def test_delete_ticket_success(self, client, sample_ticket_data):
        """Test deleting an existing ticket."""
        # Create a ticket
        create_response = client.post("/api/tickets", json=sample_ticket_data)
        ticket_id = create_response.json()["id"]
        
        # Delete the ticket
        response = client.delete(f"/api/tickets/{ticket_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        get_response = client.get(f"/api/tickets/{ticket_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_ticket_not_found(self, client):
        """Test deleting a non-existent ticket."""
        response = client.delete("/api/tickets/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestStatisticsEndpoint:
    """Tests for the GET /statistics endpoint."""

    def test_get_statistics_empty(self, client):
        """Test getting statistics with no tickets."""
        response = client.get("/api/statistics")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "total_tickets" in data
        assert data["total_tickets"] == 0
        assert "category_distribution" in data
        assert "urgency_distribution" in data

    def test_get_statistics_with_data(self, client, sample_ticket_data):
        """Test getting statistics with tickets."""
        # Create a ticket
        client.post("/api/tickets", json=sample_ticket_data)
        
        # Get statistics
        response = client.get("/api/statistics")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["total_tickets"] >= 1
        assert "average_confidence" in data


class TestHealthEndpoint:
    """Tests for the GET /health endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "database" in data
        assert "ai_service" in data
        assert data["database"] in ["healthy", "unhealthy"]
        assert data["ai_service"] in ["healthy", "unhealthy"]


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "docs" in data

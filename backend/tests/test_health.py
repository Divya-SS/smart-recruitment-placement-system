"""
Health Check API Tests.

Verifies GET /api/health endpoint behavior and response contract.
"""

import json


def test_health_check_endpoint(client):
    """
    Given a running Flask test application,
    When a GET request is sent to /api/health,
    Then it should return HTTP 200 with the expected JSON payload.
    """
    response = client.get("/api/health")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["message"] == "Smart Recruitment API is running"


def test_404_not_found(client):
    """
    Given an unknown endpoint route,
    When a client requests the route,
    Then it should return a standardized 404 JSON response.
    """
    response = client.get("/api/non-existent-endpoint")
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["status"] == "error"
    assert "not found" in data["message"].lower()

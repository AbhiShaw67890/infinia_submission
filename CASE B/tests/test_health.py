"""
Tests for the /health and /metrics endpoints.
"""


def test_health_endpoint_returns_ok(client):
    """Health endpoint should return status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "version" in data


def test_health_contains_environment(client):
    """Health response should include environment info."""
    response = client.get("/health")
    data = response.json()
    assert "environment" in data


def test_metrics_endpoint(client):
    """Metrics endpoint should return uptime and task counts."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "uptime_seconds" in data
    assert "tasks" in data
    assert data["tasks"]["total"] == 0


def test_root_endpoint(client):
    """Root endpoint should return service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data

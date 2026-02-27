"""
KamiCode — Health Check Tests
"""

import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Health endpoint should return status ok."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data

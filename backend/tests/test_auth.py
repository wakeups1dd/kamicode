"""
KamiCode — Authentication Tests

Covers registration, login, profile access, and error cases.
"""

import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    """Register a new user → 201 + access token + user data."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "SecurePass1",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["classical_rating"] == 1200
    assert data["user"]["league_tier"] == "bronze"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """Register with an already-used email → 409."""
    # First registration
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "user1",
            "email": "dup@example.com",
            "password": "SecurePass1",
        },
    )
    # Duplicate email
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "user2",
            "email": "dup@example.com",
            "password": "SecurePass1",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    """Register with an already-used username → 409."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "sameuser",
            "email": "first@example.com",
            "password": "SecurePass1",
        },
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "sameuser",
            "email": "second@example.com",
            "password": "SecurePass1",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_weak_password(client):
    """Register with a weak password → 422 (validation error)."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "weakuser",
            "email": "weak@example.com",
            "password": "short",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    """Login with correct credentials → 200 + access token."""
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "SecurePass1",
        },
    )
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "SecurePass1",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Login with incorrect password → 401."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "username": "wrongpass",
            "email": "wrongpass@example.com",
            "password": "SecurePass1",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "WrongPassword1",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_email(client):
    """Login with non-existent email → 401."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "nobody@example.com",
            "password": "SomePass123",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authenticated(client):
    """GET /me with valid token → 200 + user data."""
    # Register to get a token
    reg_response = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "meuser",
            "email": "me@example.com",
            "password": "SecurePass1",
        },
    )
    token = reg_response.json()["access_token"]

    # Access protected endpoint
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    """GET /me without token → 401."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_invalid_token(client):
    """GET /me with garbage token → 401."""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer this.is.garbage"},
    )
    assert response.status_code == 401

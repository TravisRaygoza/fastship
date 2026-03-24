from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient

from app.api.dependencies import (
    get_current_seller,
    get_seller_access_token,
    get_seller_service,
)
from app.core.exceptions import BadCredentials, InvalidToken
from app.main import app


@pytest.fixture(autouse=True)
def _cleanup_overrides():
    yield
    app.dependency_overrides.clear()


class TestSellerSignup:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, sample_seller):
        mock_service = AsyncMock()
        mock_service.add = AsyncMock(return_value=sample_seller)
        app.dependency_overrides[get_seller_service] = lambda: mock_service

        resp = await client.post(
            "/seller/signup",
            json={"name": "Test Seller", "email": "seller@test.com", "password": "pass123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Test Seller"
        assert data["email"] == "seller@test.com"
        assert "password" not in data

    @pytest.mark.asyncio
    async def test_invalid_email_422(self, client: AsyncClient):
        resp = await client.post(
            "/seller/signup",
            json={"name": "Bad", "email": "not-an-email", "password": "pass"},
        )
        assert resp.status_code == 422


class TestSellerToken:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, seller_token):
        mock_service = AsyncMock()
        mock_service.token = AsyncMock(return_value=seller_token)
        app.dependency_overrides[get_seller_service] = lambda: mock_service

        resp = await client.post(
            "/seller/token",
            data={"username": "seller@test.com", "password": "pass123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_bad_credentials_401(self, client: AsyncClient):
        mock_service = AsyncMock()
        mock_service.token = AsyncMock(side_effect=BadCredentials())
        app.dependency_overrides[get_seller_service] = lambda: mock_service

        resp = await client.post(
            "/seller/token",
            data={"username": "wrong@test.com", "password": "wrong"},
        )
        assert resp.status_code == 401


class TestSellerVerify:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient):
        mock_service = AsyncMock()
        mock_service.verify_email = AsyncMock(return_value=None)
        app.dependency_overrides[get_seller_service] = lambda: mock_service

        resp = await client.get("/seller/verify", params={"token": "sometoken"})
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Email successfully verified."

    @pytest.mark.asyncio
    async def test_invalid_token_401(self, client: AsyncClient):
        mock_service = AsyncMock()
        mock_service.verify_email = AsyncMock(side_effect=InvalidToken())
        app.dependency_overrides[get_seller_service] = lambda: mock_service

        resp = await client.get("/seller/verify", params={"token": "badtoken"})
        assert resp.status_code == 401


class TestSellerForgotPassword:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient):
        mock_service = AsyncMock()
        mock_service.send_password_reset_link = AsyncMock(return_value=None)
        app.dependency_overrides[get_seller_service] = lambda: mock_service

        resp = await client.get("/seller/forgot-password", params={"email": "seller@test.com"})
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Password reset link sent successfully."


class TestSellerLogout:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, seller_token):
        app.dependency_overrides[get_seller_access_token] = lambda: {
            "user": {"name": "Test", "id": "abc"},
            "jti": "test-jti",
        }

        resp = await client.get("/seller/logout")
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Successfully logged out"

    @pytest.mark.asyncio
    async def test_no_auth_401(self, client: AsyncClient):
        resp = await client.get("/seller/logout")
        assert resp.status_code == 401

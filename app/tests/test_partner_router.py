from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from app.api.dependencies import (
    get_current_partner,
    get_delivery_partner_access_token,
    get_delivery_partner_service,
)
from app.core.exceptions import BadCredentials
from app.main import app


@pytest.fixture(autouse=True)
def _cleanup_overrides():
    yield
    app.dependency_overrides.clear()


class TestPartnerSignup:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, sample_partner):
        mock_service = AsyncMock()
        mock_service.add = AsyncMock(return_value=sample_partner)
        app.dependency_overrides[get_delivery_partner_service] = lambda: mock_service

        resp = await client.post(
            "/partner/signup",
            json={
                "name": "Test Partner",
                "email": "partner@test.com",
                "password": "pass123",
                "serviceable_zip_codes": [10001, 10002],
                "max_handling_capacity": 10,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Test Partner"
        assert data["email"] == "partner@test.com"
        assert "password" not in data


class TestPartnerToken:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, partner_token):
        mock_service = AsyncMock()
        mock_service.token = AsyncMock(return_value=partner_token)
        app.dependency_overrides[get_delivery_partner_service] = lambda: mock_service

        resp = await client.post(
            "/partner/token",
            data={"username": "partner@test.com", "password": "pass123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_bad_credentials_401(self, client: AsyncClient):
        mock_service = AsyncMock()
        mock_service.token = AsyncMock(side_effect=BadCredentials())
        app.dependency_overrides[get_delivery_partner_service] = lambda: mock_service

        resp = await client.post(
            "/partner/token",
            data={"username": "wrong@test.com", "password": "wrong"},
        )
        assert resp.status_code == 401


class TestPartnerVerify:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient):
        mock_service = AsyncMock()
        mock_service.verify_email = AsyncMock(return_value=None)
        app.dependency_overrides[get_delivery_partner_service] = lambda: mock_service

        resp = await client.get("/partner/verify", params={"token": "sometoken"})
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Email successfully verified."


class TestPartnerUpdate:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, sample_partner):
        mock_service = AsyncMock()
        mock_service.update = AsyncMock(return_value=sample_partner)
        app.dependency_overrides[get_current_partner] = lambda: sample_partner
        app.dependency_overrides[get_delivery_partner_service] = lambda: mock_service

        resp = await client.post(
            "/partner/",
            json={"serviceable_zip_codes": [10001, 10002, 10003]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Test Partner"


class TestPartnerLogout:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient):
        app.dependency_overrides[get_delivery_partner_access_token] = lambda: {
            "user": {"name": "Test", "id": "abc"},
            "jti": "test-jti",
        }

        resp = await client.get("/partner/logout")
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Successfully logged out"

    @pytest.mark.asyncio
    async def test_no_auth_401(self, client: AsyncClient):
        resp = await client.get("/partner/logout")
        assert resp.status_code == 401

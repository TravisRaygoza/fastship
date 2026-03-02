from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

from app.api.dependencies import (
    get_current_partner,
    get_current_seller,
    get_shipment_service,
)
from app.core.exceptions import ClientNotAuthorized, EntityNotFound, NothingToUpdate
from app.main import app
from app.tests.conftest import SHIPMENT_ID


@pytest.fixture(autouse=True)
def _cleanup_overrides():
    yield
    app.dependency_overrides.clear()


def _mock_shipment_service():
    return AsyncMock()


class TestGetShipment:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, sample_seller, sample_shipment):
        mock_service = AsyncMock()
        mock_service.get = AsyncMock(return_value=sample_shipment)
        app.dependency_overrides[get_current_seller] = lambda: sample_seller
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.get(f"/shipments/{SHIPMENT_ID}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == str(SHIPMENT_ID)
        assert data["content"] == "Test Package"

    @pytest.mark.asyncio
    async def test_not_found_404(self, client: AsyncClient, sample_seller):
        mock_service = AsyncMock()
        mock_service.get = AsyncMock(side_effect=EntityNotFound())
        app.dependency_overrides[get_current_seller] = lambda: sample_seller
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.get(f"/shipments/{SHIPMENT_ID}")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_no_auth_401(self, client: AsyncClient):
        resp = await client.get(f"/shipments/{SHIPMENT_ID}")
        assert resp.status_code == 401


class TestSubmitShipment:
    @pytest.mark.asyncio
    async def test_success_201(self, client: AsyncClient, sample_seller, sample_shipment):
        mock_service = AsyncMock()
        mock_service.add = AsyncMock(return_value=sample_shipment)
        app.dependency_overrides[get_current_seller] = lambda: sample_seller
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.post(
            "/shipments/",
            json={
                "content": "Test Package",
                "weight": 5.0,
                "destination": 10002,
                "client_contact_email": "client@test.com",
                "client_contact_phone": "+1234567890",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["content"] == "Test Package"

    @pytest.mark.asyncio
    async def test_validation_error_422(self, client: AsyncClient, sample_seller):
        mock_service = AsyncMock()
        app.dependency_overrides[get_current_seller] = lambda: sample_seller
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.post("/shipments/", json={"content": "X"})
        assert resp.status_code == 422


class TestShipmentUpdate:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, sample_partner, sample_shipment):
        mock_service = AsyncMock()
        mock_service.update = AsyncMock(return_value=sample_shipment)
        app.dependency_overrides[get_current_partner] = lambda: sample_partner
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.patch(
            f"/shipments/{SHIPMENT_ID}",
            json={"status": "in_transit", "location": 10005},
        )
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_empty_body_400(self, client: AsyncClient, sample_partner):
        app.dependency_overrides[get_current_partner] = lambda: sample_partner
        mock_service = AsyncMock()
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.patch(
            f"/shipments/{SHIPMENT_ID}",
            json={},
        )
        assert resp.status_code == 400


class TestCancelShipment:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient, sample_seller, sample_shipment):
        mock_service = AsyncMock()
        mock_service.cancel = AsyncMock(return_value=sample_shipment)
        app.dependency_overrides[get_current_seller] = lambda: sample_seller
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.delete(f"/shipments/{SHIPMENT_ID}")
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_wrong_seller_401(self, client: AsyncClient, sample_seller):
        mock_service = AsyncMock()
        mock_service.cancel = AsyncMock(side_effect=ClientNotAuthorized())
        app.dependency_overrides[get_current_seller] = lambda: sample_seller
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.delete(f"/shipments/{SHIPMENT_ID}")
        assert resp.status_code == 401


class TestSubmitReview:
    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient):
        mock_service = AsyncMock()
        mock_service.rate = AsyncMock(return_value=None)
        app.dependency_overrides[get_shipment_service] = lambda: mock_service

        resp = await client.post(
            "/shipments/review",
            params={"token": "review-token"},
            data={"rating": 5, "comment": "Great delivery!"},
        )
        assert resp.status_code == 200
        assert resp.json()["detail"] == "Review submitted successfully."

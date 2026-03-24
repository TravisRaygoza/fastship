from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.database.models import DeliveryPartner, Seller, Shipment, ShipmentEvent, ShipmentStatus
from app.services.utils import generate_access_token


# ---------------------------------------------------------------------------
# Sample data fixtures
# ---------------------------------------------------------------------------

SELLER_ID = uuid4()
PARTNER_ID = uuid4()
SHIPMENT_ID = uuid4()


@pytest.fixture
def sample_seller():
    return Seller(
        id=SELLER_ID,
        name="Test Seller",
        email="seller@test.com",
        email_verified=True,
        password_hash="hashedpassword",
        address="123 Test St",
        zip_code=10001,
        created_at=datetime.now(),
        shipments=[],
    )


@pytest.fixture
def sample_partner():
    return DeliveryPartner(
        id=PARTNER_ID,
        name="Test Partner",
        email="partner@test.com",
        email_verified=True,
        password_hash="hashedpassword",
        serviceable_zip_codes=[10001, 10002],
        max_handling_capacity=10,
        created_at=datetime.now(),
        shipments=[],
    )


@pytest.fixture
def sample_shipment(sample_seller, sample_partner):
    event = ShipmentEvent(
        id=uuid4(),
        created_at=datetime.now(),
        location_zipcode=10001,
        status=ShipmentStatus.placed,
        description="Shipment created",
        shipment_id=SHIPMENT_ID,
    )
    return Shipment(
        id=SHIPMENT_ID,
        created_at=datetime.now(),
        client_contact_email="client@test.com",
        client_contact_phone="+1234567890",
        content="Test Package",
        weight=5.0,
        destination=10002,
        estimated_delivery=datetime.now(),
        seller_id=SELLER_ID,
        delivery_partner_id=PARTNER_ID,
        seller=sample_seller,
        delivery_partner=sample_partner,
        timeline=[event],
        tags=[],
    )


# ---------------------------------------------------------------------------
# Token fixtures (real JWT generation – no mocking needed)
# ---------------------------------------------------------------------------

@pytest.fixture
def seller_token():
    return generate_access_token(
        data={"user": {"name": "Test Seller", "id": str(SELLER_ID)}}
    )


@pytest.fixture
def partner_token():
    return generate_access_token(
        data={"user": {"name": "Test Partner", "id": str(PARTNER_ID)}}
    )


# ---------------------------------------------------------------------------
# Mock session fixture for service-level tests
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.get = AsyncMock()
    session.scalar = AsyncMock()
    session.execute = AsyncMock()
    return session


# ---------------------------------------------------------------------------
# ASGI test client with all external dependencies patched
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture
async def client():
    with (
        patch("app.main.create_db_tables", new_callable=AsyncMock),
        patch("app.main.add_log", new_callable=MagicMock) as mock_add_log,
        patch("app.api.dependencies.is_jti_blacklisted", new_callable=AsyncMock, return_value=False),
        patch("app.database.redis.add_jti_to_blacklist", new_callable=AsyncMock),
        patch("app.api.routers.seller.add_jti_to_blacklist", new_callable=AsyncMock),
        patch("app.api.routers.delivery_partner.add_jti_to_blacklist", new_callable=AsyncMock),
    ):
        mock_add_log.delay = MagicMock()

        from app.main import app

        async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test",
        ) as ac:
            yield ac

        app.dependency_overrides.clear()

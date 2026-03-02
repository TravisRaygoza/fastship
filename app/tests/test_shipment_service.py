from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.core.exceptions import ClientNotAuthorized, ClientNotVerified, EntityNotFound, InvalidToken
from app.database.models import (
    DeliveryPartner,
    Review,
    Seller,
    Shipment,
    ShipmentEvent,
    ShipmentStatus,
)
from app.services.shipment import ShipmentService


SELLER_ID = uuid4()
PARTNER_ID = uuid4()
SHIPMENT_ID = uuid4()


def _make_seller():
    return Seller(
        id=SELLER_ID,
        name="Seller",
        email="s@t.com",
        email_verified=True,
        password_hash="h",
        zip_code=10001,
        created_at=datetime.now(),
        shipments=[],
    )


def _make_partner():
    return DeliveryPartner(
        id=PARTNER_ID,
        name="Partner",
        email="p@t.com",
        email_verified=True,
        password_hash="h",
        serviceable_zip_codes=[10001],
        max_handling_capacity=10,
        created_at=datetime.now(),
        shipments=[],
    )


def _make_shipment(seller=None, partner=None):
    s = seller or _make_seller()
    p = partner or _make_partner()
    event = ShipmentEvent(
        id=uuid4(),
        created_at=datetime.now(),
        location_zipcode=10001,
        status=ShipmentStatus.placed,
        description="Created",
        shipment_id=SHIPMENT_ID,
    )
    return Shipment(
        id=SHIPMENT_ID,
        created_at=datetime.now(),
        client_contact_email="c@t.com",
        client_contact_phone="+1",
        content="Pkg",
        weight=5.0,
        destination=10002,
        estimated_delivery=datetime.now(),
        seller_id=SELLER_ID,
        delivery_partner_id=PARTNER_ID,
        seller=s,
        delivery_partner=p,
        timeline=[event],
        tags=[],
    )


def _build_service(session):
    partner_service = AsyncMock()
    event_service = AsyncMock()
    return ShipmentService(session, partner_service, event_service), partner_service, event_service


class TestShipmentServiceGet:
    @pytest.mark.asyncio
    async def test_returns_shipment(self, mock_session):
        shipment = _make_shipment()
        mock_session.get = AsyncMock(return_value=shipment)
        svc, _, _ = _build_service(mock_session)

        result = await svc.get(SHIPMENT_ID)
        assert result.id == SHIPMENT_ID

    @pytest.mark.asyncio
    async def test_not_found_raises(self, mock_session):
        mock_session.get = AsyncMock(return_value=None)
        svc, _, _ = _build_service(mock_session)

        with pytest.raises(EntityNotFound):
            await svc.get(SHIPMENT_ID)


class TestShipmentServiceAdd:
    @pytest.mark.asyncio
    async def test_assigns_partner_and_creates_event(self, mock_session):
        seller = _make_seller()
        partner = _make_partner()
        svc, partner_svc, event_svc = _build_service(mock_session)

        partner_svc.assign_shipment = AsyncMock(return_value=partner)

        event = ShipmentEvent(
            id=uuid4(),
            created_at=datetime.now(),
            location_zipcode=10001,
            status=ShipmentStatus.placed,
            description="placed",
            shipment_id=SHIPMENT_ID,
        )
        event_svc.add = AsyncMock(return_value=event)

        # _add persists and returns the shipment; mock it to just return input
        async def fake_add(entity):
            entity.id = SHIPMENT_ID
            entity.timeline = []
            return entity

        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        mock_session.add = MagicMock()

        with patch.object(svc, "_add", side_effect=fake_add):
            shipment_create = ShipmentCreate(
                content="Box",
                weight=5.0,
                destination=10002,
                client_contact_email="c@t.com",
            )
            result = await svc.add(shipment_create, seller)

        partner_svc.assign_shipment.assert_called_once()
        event_svc.add.assert_called_once()
        assert result.seller_id == SELLER_ID


class TestShipmentServiceUpdate:
    @pytest.mark.asyncio
    async def test_wrong_partner_raises(self, mock_session):
        shipment = _make_shipment()
        mock_session.get = AsyncMock(return_value=shipment)
        svc, _, _ = _build_service(mock_session)

        other_partner = _make_partner()
        other_partner.id = uuid4()

        update = ShipmentUpdate(status=ShipmentStatus.in_transit, location=10005)

        with pytest.raises(ClientNotAuthorized):
            await svc.update(SHIPMENT_ID, update, other_partner)

    @pytest.mark.asyncio
    @patch("app.services.shipment.get_shipment_verification_code", new_callable=AsyncMock)
    async def test_delivery_requires_verification_code(self, mock_get_code, mock_session):
        shipment = _make_shipment()
        mock_session.get = AsyncMock(return_value=shipment)
        svc, _, event_svc = _build_service(mock_session)
        event_svc.add = AsyncMock()

        mock_get_code.return_value = "123456"

        partner = _make_partner()
        update = ShipmentUpdate(
            status=ShipmentStatus.delivered, verification_code="999999"
        )

        with pytest.raises(ClientNotVerified):
            await svc.update(SHIPMENT_ID, update, partner)


class TestShipmentServiceCancel:
    @pytest.mark.asyncio
    async def test_wrong_seller_raises(self, mock_session):
        shipment = _make_shipment()
        mock_session.get = AsyncMock(return_value=shipment)
        svc, _, _ = _build_service(mock_session)

        other_seller = _make_seller()
        other_seller.id = uuid4()

        with pytest.raises(ClientNotAuthorized):
            await svc.cancel(SHIPMENT_ID, other_seller)

    @pytest.mark.asyncio
    async def test_creates_cancelled_event(self, mock_session):
        shipment = _make_shipment()
        mock_session.get = AsyncMock(return_value=shipment)
        svc, _, event_svc = _build_service(mock_session)

        cancelled_event = ShipmentEvent(
            id=uuid4(),
            created_at=datetime.now(),
            location_zipcode=10001,
            status=ShipmentStatus.cancelled,
            description="cancelled",
            shipment_id=SHIPMENT_ID,
        )
        event_svc.add = AsyncMock(return_value=cancelled_event)

        seller = _make_seller()
        result = await svc.cancel(SHIPMENT_ID, seller)

        event_svc.add.assert_called_once()
        call_kwargs = event_svc.add.call_args
        assert call_kwargs.kwargs.get("status") == ShipmentStatus.cancelled


class TestShipmentServiceRate:
    @pytest.mark.asyncio
    async def test_invalid_token_raises(self, mock_session):
        svc, _, _ = _build_service(mock_session)

        with pytest.raises(InvalidToken):
            await svc.rate("bad-token", 5, "Great")

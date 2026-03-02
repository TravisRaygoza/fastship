from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.api.schemas.seller import SellerCreate
from app.core.exceptions import BadCredentials, ClientNotVerified, InvalidToken
from app.database.models import Seller
from app.services.seller import SellerService


SELLER_ID = uuid4()


def _make_verified_seller(password_hash):
    return Seller(
        id=SELLER_ID,
        name="Seller",
        email="s@test.com",
        email_verified=True,
        password_hash=password_hash,
        created_at=datetime.now(),
        shipments=[],
    )


def _make_unverified_seller(password_hash):
    seller = _make_verified_seller(password_hash)
    seller.email_verified = False
    return seller


class TestSellerServiceAdd:
    @pytest.mark.asyncio
    @patch("app.services.user.send_email_with_template")
    async def test_hashes_password_and_sends_email(self, mock_email_task, mock_session):
        mock_email_task.delay = MagicMock()

        async def fake_add(entity):
            entity.id = SELLER_ID
            return entity

        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        mock_session.add = MagicMock()

        svc = SellerService(mock_session)

        with patch.object(svc, "_add", side_effect=fake_add):
            seller_data = SellerCreate(name="New Seller", email="new@test.com", password="secret123")
            result = await svc.add(seller_data)

        assert result.name == "New Seller"
        assert result.password_hash != "secret123"  # should be hashed
        mock_email_task.delay.assert_called_once()


class TestSellerServiceToken:
    @pytest.mark.asyncio
    async def test_valid_credentials_returns_jwt(self, mock_session):
        from app.services.user import password_context

        hashed = password_context.hash("correct-password")
        seller = _make_verified_seller(hashed)
        mock_session.scalar = AsyncMock(return_value=seller)

        svc = SellerService(mock_session)
        token = await svc.token("s@test.com", "correct-password")

        assert isinstance(token, str)
        assert len(token) > 0

    @pytest.mark.asyncio
    async def test_wrong_password_raises(self, mock_session):
        from app.services.user import password_context

        hashed = password_context.hash("correct-password")
        seller = _make_verified_seller(hashed)
        mock_session.scalar = AsyncMock(return_value=seller)

        svc = SellerService(mock_session)

        with pytest.raises(BadCredentials):
            await svc.token("s@test.com", "wrong-password")

    @pytest.mark.asyncio
    async def test_unverified_email_raises(self, mock_session):
        from app.services.user import password_context

        hashed = password_context.hash("password")
        seller = _make_unverified_seller(hashed)
        mock_session.scalar = AsyncMock(return_value=seller)

        svc = SellerService(mock_session)

        with pytest.raises(ClientNotVerified):
            await svc.token("s@test.com", "password")

    @pytest.mark.asyncio
    async def test_nonexistent_user_raises(self, mock_session):
        mock_session.scalar = AsyncMock(return_value=None)

        svc = SellerService(mock_session)

        with pytest.raises(BadCredentials):
            await svc.token("nobody@test.com", "any")


class TestSellerServiceVerifyEmail:
    @pytest.mark.asyncio
    async def test_invalid_token_raises(self, mock_session):
        svc = SellerService(mock_session)

        with pytest.raises(InvalidToken):
            await svc.verify_email("bad-token-string")

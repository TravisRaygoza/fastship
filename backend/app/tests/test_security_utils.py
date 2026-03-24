from datetime import timedelta

import pytest

from app.core.exceptions import InvalidToken
from app.services.utils import (
    decode_access_token,
    decode_url_safe_token,
    generate_access_token,
    generate_url_safe_token,
)


class TestAccessToken:
    def test_roundtrip(self):
        data = {"user": {"name": "Alice", "id": "abc-123"}}
        token = generate_access_token(data)
        decoded = decode_access_token(token)
        assert decoded["user"]["name"] == "Alice"
        assert decoded["user"]["id"] == "abc-123"
        assert "jti" in decoded
        assert "exp" in decoded

    def test_expired_token_raises_invalid_token(self):
        token = generate_access_token(
            {"user": {"name": "Bob", "id": "x"}},
            expiry=timedelta(seconds=-1),
        )
        with pytest.raises(InvalidToken):
            decode_access_token(token)

    def test_invalid_string_returns_none(self):
        assert decode_access_token("not.a.valid.jwt") is None

    def test_empty_string_returns_none(self):
        assert decode_access_token("") is None

    def test_token_contains_jti(self):
        token = generate_access_token({"user": {"name": "C", "id": "1"}})
        decoded = decode_access_token(token)
        assert isinstance(decoded["jti"], str)
        assert len(decoded["jti"]) > 0


class TestUrlSafeToken:
    def test_roundtrip(self):
        data = {"email": "a@b.com", "id": "123"}
        token = generate_url_safe_token(data)
        decoded = decode_url_safe_token(token)
        assert decoded == data

    def test_roundtrip_with_salt(self):
        data = {"id": "456"}
        token = generate_url_safe_token(data, salt="password-reset")
        decoded = decode_url_safe_token(token, salt="password-reset")
        assert decoded == data

    def test_wrong_salt_returns_none(self):
        token = generate_url_safe_token({"id": "1"}, salt="correct-salt")
        assert decode_url_safe_token(token, salt="wrong-salt") is None

    def test_invalid_token_returns_none(self):
        assert decode_url_safe_token("garbage-token") is None

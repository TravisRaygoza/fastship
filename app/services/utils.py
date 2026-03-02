from datetime import datetime, timedelta, timezone
from pathlib import Path
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
import jwt
from uuid import uuid4

from app.config import security_settings
from app.core.exceptions import InvalidToken

_serializer = URLSafeTimedSerializer(security_settings.JWT_SECRET_KEY)


APP_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = APP_DIR / "templates"
TEMPLATE_DIR_PASSWORD_RESET = TEMPLATE_DIR / "password"


def generate_access_token(data: dict, expiry: timedelta = timedelta(days=1)) -> str:
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )

    # If token has expired, return http exception
    except jwt.ExpiredSignatureError:
        raise InvalidToken() # Raise custom exception for invalid token

    # If token is invalid or expired, return None
    except jwt.PyJWTError:
        return None


def generate_url_safe_token(
    data: dict,
    salt: str | None = None,
) -> str:
    return _serializer.dumps(data, salt=salt)


def decode_url_safe_token(
    token: str,
    salt: str | None = None,
    expiry: timedelta | None = None,
) -> dict | None:
    try:
        return _serializer.loads(
            token,
            salt=salt,
            max_age=expiry.total_seconds() if expiry else None,
        )
    except (BadSignature, SignatureExpired):
        return None

from datetime import timedelta
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from passlib.context import CryptContext

from app.core.exceptions import BadCredentials, ClientNotVerified, InvalidToken
from app.database.models import User
from app.services.base import BaseService
from app.services.utils import (
    decode_url_safe_token,
    generate_access_token,
    generate_url_safe_token,
)
from app.config import app_settings
from app.worker.tasks import send_email_with_template


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession, ):
        # Get database session to perform database operations
        self.model = model
        self.session = session
       

    async def _add_user(self, data: dict, router_prefix: str):
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"]),
        )
        user = await self._add(user)

        token = generate_url_safe_token({"email": user.email, "id": str(user.id)})

        send_email_with_template.delay(
            recipients=[user.email],
            subject="Verify your email address",
            context={
                "username": user.name,
                "verification_url": f"http://{app_settings.APP_DOMAIN}/{router_prefix}/verify?token={token}",
            },
            template_name="mail_email_verify.html",
        )

        return user

    async def verify_email(self, token: str):
        token_data = decode_url_safe_token(token)

        if not token_data:
            raise InvalidToken() # Raise custom exception for invalid token

        user = await self._get(UUID(token_data["id"]))

        user.email_verified = True

        return await self._update(user)



    async def _get_by_email(self, email) -> User | None:
        # Validate the credentials
        return await self.session.scalar(
            # Using a custom sql query to fetch the user by email
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:
        user = await self._get_by_email(email)

        # To check if user is correct or exists and verify password
        if user is None or not password_context.verify(
            password,
            user.password_hash,
        ):
            raise BadCredentials() # Raise custom exception for bad credentials

        # If credentials are valid, generate and return a token

        # To check if email is verified
        if not user.email_verified:
            raise ClientNotVerified() ## Raise custom exception if not verified

        return generate_access_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                }
            }
        )

    async def send_password_reset_link(self, email, router_prefix: str):
        user = await self._get_by_email(email)

        token = generate_url_safe_token({"id": str(user.id)}, salt="password-reset")

        send_email_with_template.delay(
            recipients=[user.email],
            subject="Password Reset Request",
            context={
                "username": user.name,
                "reset_url": f"http://{app_settings.APP_DOMAIN}{router_prefix}/reset-password-form?token={token}",
            },
            template_name="mail_password_reset.html",
        )

    async def reset_password(self, token: str, new_password: str) -> bool:
        token_data = decode_url_safe_token(
            token,
            salt="password-reset",
            expiry=timedelta(days=1),

        )
        if not token_data:
            return False


        user = await self._get(UUID(token_data["id"]))

        user.password_hash = password_context.hash(new_password)

        await self._update(user)
        
        return True
    

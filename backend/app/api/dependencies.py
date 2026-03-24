from typing import Annotated
from uuid import UUID
from app.core.exceptions import ClientNotAuthorized, InvalidToken
from app.database.models import DeliveryPartner, Seller
from app.database.redis import is_jti_blacklisted
from app.services.delivery_partner import DeliveryPartnerService
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session

from app.core.security import oauth2_scheme_seller, oauth2_scheme_partner
from app.services.shipment_event import ShipmentEventService
from app.services.utils import decode_access_token


# Async database Session Dependency Annotation
SessionDependency = Annotated[AsyncSession, Depends(get_session)]
### This is pretty much the following: Session = Depends(get_session)


# Access Token Dependency
async def _get_access_token(token: str) -> dict:
    data = decode_access_token(token)

    # Validate token data
    if data is None or await is_jti_blacklisted(data["jti"]):
        raise InvalidToken() # Raise custom exception for invalid token

    return data


# Seller Access Token Data
async def get_seller_access_token(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
) -> dict:
    return await _get_access_token(token)


# Delivery Access Token Data
async def get_delivery_partner_access_token(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
) -> dict:
    return await _get_access_token(token)


# Logged-In Seller Dependency
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDependency,
):
    seller = await session.get(Seller, UUID(token_data["user"]["id"]))

    if seller is None:
        raise ClientNotAuthorized() # Raise custom exception for unauthorized client

    return seller


# Logged-In Delivery Partner Dependency
async def get_current_partner(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
    session: SessionDependency,
):
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))

    if partner is None:
        raise ClientNotAuthorized() # Raise custom exception for unauthorized client

    return partner


### Service Dependencies ###
# Shipment service dependency
def get_shipment_service(session: SessionDependency):
    return ShipmentService(
        session,
        DeliveryPartnerService(session),
        ShipmentEventService(session),
    )

# Seller service dependency
def get_seller_service(session: SessionDependency):
    return SellerService(session)

# Delivery Partner Dependency
def get_delivery_partner_service(session: SessionDependency):
    return DeliveryPartnerService(session)


### Dependency Annotations ###

# Seller Dependency Annotation
seller_dependency = Annotated[
    Seller,
    Depends(get_current_seller),
]

# Delivery Partner Dependency Annotation
deliveryPartner_dependency = Annotated[
    DeliveryPartner,
    Depends(get_current_partner),
]

# Shipment service dependency annotation
shipment_dependency = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]


# Seller service dependency annotation
seller_service_dependency = Annotated[
    SellerService,
    Depends(get_seller_service),
]

# Delivery Partner service dependency annotation
deliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService,
    Depends(get_delivery_partner_service),
]
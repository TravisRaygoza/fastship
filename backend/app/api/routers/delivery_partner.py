from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.core.exceptions import DeliveryPartnerNotAvailable
from app.database.redis import add_jti_to_blacklist
from app.services.utils import TEMPLATE_DIR
from app.config import app_settings

from ..schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from ..dependencies import (
    get_delivery_partner_access_token,
    deliveryPartner_dependency,
    deliveryPartnerServiceDep
)


router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


# create an endpoint to create a delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    partner: DeliveryPartnerCreate,
    service: deliveryPartnerServiceDep,
):
    return await service.add(partner)


#### Login the delivery partner
@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: deliveryPartnerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


#### Verify Delivery Partner Email
@router.get("/verify")
async def verify_delivery_partner_email(request: Request, token: str, service: deliveryPartnerServiceDep):
    await service.verify_email(token)

    templates = Jinja2Templates(TEMPLATE_DIR)
    return templates.TemplateResponse(
        request=request,
        name="email_verified.html",
        context={"login_url": f"http://{app_settings.APP_DOMAIN}/partner/login"}
    )



### Update the delivery partner details
@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: deliveryPartner_dependency,
    service: deliveryPartnerServiceDep,
):
    update = partner_update.model_dump(exclude_none=True)

    if not update:
        raise DeliveryPartnerNotAvailable() # Raise custom exception if no data to update
    return await service.update(
        partner.sqlmodel_update(update)
    )

### Logout the delivery partner
@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_delivery_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])

    return {"detail": "Successfully logged out"}

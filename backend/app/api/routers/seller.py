from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.database.redis import add_jti_to_blacklist
from app.services.utils import TEMPLATE_DIR
from app.config import app_settings


from ..schemas.seller import SellerCreate, SellerRead
from ..dependencies import get_seller_access_token, seller_service_dependency


router = APIRouter(prefix="/seller", tags=["Seller"])


# create an endpoint to create a seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: seller_service_dependency):
    return await service.add(seller)


#### Login the seller
@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: seller_service_dependency,
):
    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


#### Verify Seller Email
@router.get("/verify")
async def verify_seller_email(token: str, service: seller_service_dependency):
    await service.verify_email(token)

    return {"detail": "Email successfully verified."}


#### Password Reset Link
@router.get("/forgot-password")
async def forgot_password(email: EmailStr, service: seller_service_dependency):
    await service.send_password_reset_link(email, router.prefix)

    return {"detail": "Password reset link sent successfully."}


### Password Reset Form
@router.get("/reset-password-form")
async def reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset-password?token={token}"
        })

### Reset Seller Password
@router.post("/reset-password")
async def reset_password(request: Request, token: str, password: Annotated[str, Form()], service: seller_service_dependency):
    is_successful = await service.reset_password(token, password)
    
    templates = Jinja2Templates(TEMPLATE_DIR)

    
    return templates.TemplateResponse(
        request=request,
        name="password/reset_success.html" if is_successful else "password/reset_failed.html",
    )


### Logout the seller
@router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_seller_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])

    return {"detail": "Successfully logged out"}



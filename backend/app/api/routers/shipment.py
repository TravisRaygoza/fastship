### This is the router.py file to define API routes


from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Form, Request, status

from app.config import app_settings
from fastapi.templating import Jinja2Templates

from app.api.schemas.shipment import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)
from app.core.exceptions import NothingToUpdate
from app.database.models import Shipment, TagName
from app.api.dependencies import (
    SessionDependency,
    shipment_dependency,
    seller_dependency,
    deliveryPartner_dependency,
)
from app.services.utils import TEMPLATE_DIR


router = APIRouter(prefix="/shipments", tags=["shipments"])

templates = Jinja2Templates(TEMPLATE_DIR)


### Tracking details of shipment
@router.get("/track")
async def get_tracking(request: Request, id: UUID, service: shipment_dependency):
    # Check for shipment with given id
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context,
    )


### Get all shipments with a tag
@router.get("/tagged", response_model=list[ShipmentRead])
async def get_shipments_with_tag(
    tag_name: TagName,
    session: SessionDependency,
):
    tag = await tag_name.tag(session)
    tag.shipments

    return tag.shipments


### Add a tag to a shipment
@router.get("/tag", response_model=ShipmentRead)
async def add_tag_to_shipment(
    id: UUID,
    tag: TagName,
    service: shipment_dependency,
):
    return await service.add_tag(id, tag)


### Remove a tag from a shipment
@router.delete("/tag", response_model=ShipmentRead)
async def remove_tag_from_shipment(
    id: UUID,
    tag: TagName,
    service: shipment_dependency,
):
    return await service.remove_tag(id, tag)


### Submit a review for a shipment
@router.get("/review")
async def submit_review_page(request: Request, token: str):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url": f"http://{app_settings.APP_DOMAIN}/shipments/review?token={token}"
        }
    )

### Submit a review for a shipment
@router.post("/review")
async def submit_review(
    token: str,
    rating: Annotated[int, Form(ge=1, le=5)],
    comment: Annotated[str | None, Form()],
    service: shipment_dependency,
):
    await service.rate(token, rating, comment)
    return {"detail": "Review submitted successfully."}

############Adding view to see all shipments for seller and partner######
@router.get("/seller", response_model=list[ShipmentRead])
async def get_all_seller_shipments(seller: seller_dependency):
    return seller.shipments

@router.get("/partner", response_model=list[ShipmentRead])
async def get_all_partner_shipments(partner: deliveryPartner_dependency):
    return partner.shipments


# This is a post endpoint to create a new shipment
@router.post("/", response_model=ShipmentRead, status_code=status.HTTP_201_CREATED)
async def submit_shipment(
    seller: seller_dependency,
    shipment: ShipmentCreate,
    service: shipment_dependency,
) -> Shipment:
    return await service.add(shipment, seller)



@router.get("/{id}", response_model=ShipmentRead, status_code=status.HTTP_200_OK)
async def get_shipment(
    id: UUID, _: seller_dependency, service: shipment_dependency
) -> Shipment:
    return await service.get(id)


@router.patch("/{id}", response_model=ShipmentRead)
async def shipment_update(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: deliveryPartner_dependency,
    service: shipment_dependency,
):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    ## Raise an error if no fields are provided for update
    if not update:
        raise NothingToUpdate()

    return await service.update(id, shipment_update, partner)


### Cancel a shipment by id
@router.delete("/{id}", response_model=ShipmentRead)
async def delete_shipment(
    id: UUID,
    seller: seller_dependency,
    service: shipment_dependency,
) -> Shipment:
    return await service.cancel(id, seller)

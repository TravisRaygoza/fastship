import datetime

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.core.exceptions import ClientNotAuthorized, ClientNotVerified, EntityNotFound, InvalidToken
from app.database.models import DeliveryPartner, Review, Seller, Shipment, ShipmentStatus, TagName
from app.database.redis import get_shipment_verification_code
from app.services.delivery_partner import DeliveryPartnerService
from app.services.shipment_event import ShipmentEventService
from app.services.utils import decode_url_safe_token

from .base import BaseService


class ShipmentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService,
    ):
        # Initialize the base service with the Shipment model and database session
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service

    # Get Shipment by id
    async def get(self, id: UUID) -> Shipment | None:
        shipment =  await self._get(id)
        if not shipment:
            raise EntityNotFound() # Raise custom exception if not found
        
        return shipment
        

    # Create a new Shipment
    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,  # default status for new shipments
            estimated_delivery=datetime.datetime.now()
            + datetime.timedelta(days=3),  # default estimated delivery date
            seller_id=seller.id,
        )
        partner = await self.partner_service.assign_shipment(new_shipment)

        new_shipment.delivery_partner_id = partner.id

        shipment = await self._add(new_shipment)
        event = await self.event_service.add(
            shipment=shipment,
            location=seller.zip_code,
            status=ShipmentStatus.placed,
            description=f"Shipment created and assigned to delivery {partner.name}",
        )

        shipment.timeline.append(event)

        return shipment

    # Update an existing Shipment
    async def update(
        self,
        id: UUID,
        shipment_update: ShipmentUpdate,
        partner: DeliveryPartner,
    ) -> Shipment:
        # Validate logged in partner with assigned partner
        # On the shipment with given id
        shipment = await self.get(id)

        if shipment.delivery_partner_id != partner.id:
            raise ClientNotAuthorized() ## Raise custom exception if not authorized
        
        if shipment_update.status == ShipmentStatus.delivered:
            code = await get_shipment_verification_code(shipment.id)

            if code != shipment_update.verification_code:
                raise ClientNotVerified() ## Raise custom exception if not verified

        update = shipment_update.model_dump(exclude_none=True, exclude={"verification_code"})

        #update estimated delivery if provided
        if shipment_update.estimated_delivery is not None:
            shipment.estimated_delivery = shipment_update.estimated_delivery
        
        if len(update) > 1 or not shipment_update.estimated_delivery:
            await self.event_service.add(
                shipment=shipment,
                **update,
            )


        return await self._update(shipment)

    ### TAGS ###
    async def add_tag(self, id: UUID, tag: TagName):
        shipment = await self.get(id)

        shipment.tags.append(await tag.tag(self.session))
        return await self._update(shipment)

    async def remove_tag(self, id: UUID, tag: TagName):
        shipment = await self.get(id)

        try:
            shipment.tags.remove(await tag.tag(self.session))
        except ValueError:
            raise EntityNotFound() ## Raise custom exception if tag not found on shipment

        return await self._update(shipment)

    #### Rating a shipment ####
    async def rate(self, token: str, rating: int, comment: str) -> None:
        token_data = decode_url_safe_token(token)

        if not token_data:
            raise InvalidToken()
        
        shipment = await self.get(UUID(token_data["id"]))

        new_review = Review(
            rating=rating,
            comment=comment if comment else None,
            shipment_id= shipment.id,
        )

        self.session.add(new_review)
        await self.session.commit()






    async def cancel(self, id: UUID, seller: Seller) -> Shipment:
        # Validate the seller
        shipment = await self._get(id)

        if shipment.seller_id != seller.id:
            raise ClientNotAuthorized() ## Raise custom exception if not authorized
        
        event = await self.event_service.add(
            shipment=shipment,
            status=ShipmentStatus.cancelled,
        )

        shipment.timeline.append(event)
        return shipment


    # Delete a Shipment by id
    async def delete(self, id: UUID) -> None:
        await self._delete(await self._get(id))
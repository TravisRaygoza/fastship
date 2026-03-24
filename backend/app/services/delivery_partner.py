from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Sequence, select, any_


from app.api.schemas.delivery_partner import DeliveryPartnerCreate
from app.core.exceptions import DeliveryPartnerCapacityExceeded, DeliveryPartnerNotAvailable
from app.database.models import DeliveryPartner, Shipment
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(model=DeliveryPartner, session=session)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        return await self._add_user(delivery_partner.model_dump(), "partner")

    async def get_partners_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        result = (
            await self.session.execute(
                select(DeliveryPartner).where(
                    zipcode == any_(DeliveryPartner.serviceable_zip_codes)
                )
            )
        )
        return result.scalars().all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partners_by_zipcode(shipment.destination)
        
        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner

        raise DeliveryPartnerNotAvailable() # Raise custom exception if no partners available

    async def update(self, delivery_partner: DeliveryPartner):
        return await self._update(delivery_partner)

    async def token(self, email, password) -> str:
        return await self._generate_token(email, password)

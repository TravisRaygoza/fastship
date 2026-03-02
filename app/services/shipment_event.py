
from random import randint

from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.database.redis import add_shipment_verification_code
from app.services.base import BaseService
from app.config import app_settings
from app.services.utils import generate_url_safe_token
from app.worker.tasks import send_email_with_template, send_sms

class ShipmentEventService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent, session)
        

    async def add(
        self,
        shipment: Shipment,
        location: int = None,
        status: ShipmentStatus = None,
        description: str | None = None,
    ) -> ShipmentEvent:
        if not location or not status:
            last_event = await self.get_latest_event(shipment)
            if last_event:
                location = location if location else last_event.location_zipcode
                status = status if status else last_event.status
            else: 
                location = location if location else shipment.destination
                status = status if status else ShipmentStatus.placed

        new_event = ShipmentEvent(
            location_zipcode=location,
            status=status,
            description=description
            if description
            else self._generate_description(
                status,
                location,
            ),
            shipment_id=shipment.id,
        )

        await self._notify_user(shipment, status)

        return await self._add(new_event)

    async def get_latest_event(self, shipment: Shipment):
        timeline = shipment.timeline
        #Empty Check 
        if not timeline:
            return None
        
        timeline.sort(key=lambda event: event.created_at)
        return timeline[-1]

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.out_for_delivery:
                return "shipment is out for delivery"
            case ShipmentStatus.delivered:
                return "shipment has been delivered"
            case ShipmentStatus.cancelled:
                return "shipment has been cancelled by the seller"
            case _:  # and ShipmentStatus.in_transit
                return f"shipment scanned at {location}"

    async def _notify_user(self, shipment: Shipment, status: ShipmentStatus):
        
        if status == ShipmentStatus.in_transit:
            return  # No notification for in_transit status

        subject: str
        context = {}
        template_name: str


        match status:

            case ShipmentStatus.placed:
                subject="Your order has been placed"
                context["order_id"] = shipment.id
                context["seller"] = shipment.seller.name
                context["partner"] = shipment.delivery_partner.name
                template_name="mail_placed.html"
            
            case ShipmentStatus.out_for_delivery:
                subject="Your order is out for delivery"
                context["seller"] = shipment.seller.name
                context["partner"] = shipment.delivery_partner.name
                template_name="mail_out_for_delivery.html"

                code = randint(100_000, 999_999)
                await add_shipment_verification_code(shipment.id, code)
                
                context["verification_code"] = code
                
                if shipment.client_contact_phone:
                    send_sms.delay(
                        to=shipment.client_contact_phone,
                        body=f"Your verification code for order {shipment.id} is {code}",
                    )
                
                    


            case ShipmentStatus.delivered:
                subject="Your order has been delivered"
                context["seller"] = shipment.seller.name
                token = generate_url_safe_token({"id": str(shipment.id)})
                context["review_url"] = f"{app_settings.APP_DOMAIN}/shipments/review?token={token}"
                template_name="mail_delivered.html"
            case ShipmentStatus.cancelled:
                subject="Your order has been cancelled"
                context["seller"] = shipment.seller.name
                template_name="mail_cancelled.html"
            
        
        if shipment.client_contact_email:
            send_email_with_template.delay(
                recipients=[shipment.client_contact_email],
                subject=subject,
                context=context,
                template_name=template_name,
            )
        

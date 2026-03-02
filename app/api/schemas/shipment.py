from datetime import datetime

from uuid import UUID

from pydantic import BaseModel, Field

from app.database.models import Seller, ShipmentEvent, ShipmentStatus, Tag, TagName


#There was a lot of repetition in the code for the pydantic models, 
# So we will inherit from a base model to reduce redundancy
class RepetitiveFields(BaseModel):
    content: str = Field(
        description="Content of the shipment",
        max_length=50,
    )
    weight: float = Field(
        description="Weight of the shipment in lbs",
        lt=50,
        ge=0.5,
    )  # weight must be less than 50
    destination: int = Field(
        description="Destination zip code of the shipment",
    )  # default random destination

# class ShipmentEventRead(BaseModel):
#     id: UUID
#     created_at: datetime
#     location_zipcode: int
#     status: ShipmentStatus
#     description: str
#     shipment_id: UUID

#     model_config = ConfigDict(from_attributes=True)
    


#There are two types of pydantic models: 
# 1. Request Body Models: Used to validate and parse the data sent in the body of HTTP requests (e.g., POST, PUT).
# 2. Response Models: Used to validate and format the data sent back in the HTTP responses.

class TagRead(BaseModel):
    name: TagName
    instruction: str



# Create a pydantic model for shipment data validation
# This pydantic is a request body schema for creating a new shipment
class ShipmentRead(RepetitiveFields):
    id: UUID
    seller: Seller
    timeline: list[ShipmentEvent] = []
    estimated_delivery : datetime
    tags: list[Tag] = Field(
        default_factory=list,
        description="List of tags associated with the shipment",
    )


# default_factory is used to call a function to generate a default value
# the function is not being called during the class definition, but rather when an instance of the class is created without providing a value for that field.
# You can add more schemas as needed for other endpoints.



###### Response Model #######

# This pydantic model is for create a shipment response
class ShipmentCreate(RepetitiveFields):
    client_contact_email: str | None = Field(
        description="Contact email of the client",
        max_length=100,
    )  # contact email of the client
    
    client_contact_phone: str | None = Field(default=None,
        description="Contact phone number of the client",
    )  # contact phone number of the client
    

# This pydantic model is for the update shipment response 
class ShipmentUpdate(BaseModel):
    location: int | None = Field(default=None,
        description="Current location zip code of the shipment",
    )  # location of the shipment 
    description: str | None = Field(default=None,
        description="Description of the shipment status",
    )  # description of the shipment status
    status: ShipmentStatus | None = Field(default=None,
        description="Current status of the shipment",
    )  # status of the shipment
    verification_code: str | None = Field(default=None,
        description="Verification code for delivery confirmation",
    )  # verification code for delivery confirmation
    estimated_delivery: datetime | None = Field(default=None, 
        description="Estimated delivery date of the shipment",
    )  # estimated delivery date of the shipment


class ShipmentReview(BaseModel):
    rating: int = Field(
        description="Rating for the shipment",
        ge=1,
        le=5,
    )  # rating must be between 1 and 5
    comment: str | None = Field(default=None,
        description="Comment for the shipment review",)
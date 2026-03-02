from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Column, Relationship, SQLModel, Field, select
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, INTEGER
from sqlalchemy.ext.asyncio import AsyncSession


class TagName(str, Enum):
    EXPRESS = "express"
    STANDARD = "standard"
    FRAGILE = "fragile"
    HEAVY = "heavy"
    INTERNATIONAL = "international"
    DOMESTIC = "domestic"
    TEMPERATURE_CONTROLLED = "temperature_controlled"
    GIFT = "gift"
    RETURN = "return"
    DOCUMENTS = "documents"

    async def tag(self, session: AsyncSession):
        return await session.scalar(
            select(Tag).where(Tag.name == self.value)
        )

# Create an ENUM for shipment status
# This helps to restrict the status values to predefined options
# Inside the parentheses, we define them as string values.
# Remember that Enum members are constants and should be in lowercase.
# Also it can only be one type of value, either str or int.
class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"


class ShipmentTagLink(SQLModel, table=True):
    __tablename__ = "shipment_tag_link"

    shipment_id: UUID = Field(
        foreign_key="shipment.id", primary_key=True
    )
    tag_id: UUID = Field(
        foreign_key="tag.id", primary_key=True
    )
   
class Tag(SQLModel, table=True):
    __tablename__ = "tag"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    name: TagName
    instruction: str 

    shipments: list["Shipment"] = Relationship(
        back_populates="tags",
        link_model=ShipmentTagLink,
        sa_relationship_kwargs={"lazy": "immediate"},
    )




#### Models ####

# Shipment model and table in the database 
class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    # This is for email content
    client_contact_email: EmailStr | None
    client_contact_phone: str | None


    content: str
    weight: float = Field(ge=0.5, lt=50)
    destination: int
    estimated_delivery: datetime

    timeline: list["ShipmentEvent"] = Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )

    delivery_partner_id: UUID | None = Field(
        default=None,
        foreign_key="delivery_partner.id",
    )

    delivery_partner: Optional["DeliveryPartner"] = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    review: Optional["Review"] = Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    tags: list[Tag] = Relationship(
        back_populates="shipments",
        link_model=ShipmentTagLink,
        sa_relationship_kwargs={"lazy": "immediate"},
    )

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None


# 
class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_event"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    location_zipcode: int
    status: ShipmentStatus
    description: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipment.id")

    shipment: Shipment = Relationship(
        back_populates="timeline",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

###This class will not be made into a table, 
### So, we will only use it to inherit common fields. 
class User(SQLModel):
    name: str

    email: EmailStr
    email_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)

# Seller model and table in the database
### This class inherits from User and will be a table in the database.
class Seller(User, table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    address: str | None = Field(default=None)
    zip_code: int | None = Field(default=None)


    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# DeliveryPartner model and table in the database 
### This class also inherits the fields from User. 
class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    serviceable_zip_codes: list[int] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(INTEGER), server_default="{}"),

    )
    max_handling_capacity: int

    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
            and shipment.status != ShipmentStatus.cancelled
        ]
    
    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)

class Review(SQLModel, table=True):
    __tablename__ = "review"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipment.id")
    shipment: Shipment = Relationship(
        back_populates="review",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from database import Base

class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linked_id = Column(Integer, ForeignKey("contact.id"), nullable=True)
    link_precedence = Column(String, CheckConstraint("link_precedence IN ('primary','secondary')"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

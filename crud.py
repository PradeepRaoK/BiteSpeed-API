from sqlalchemy.orm import Session
import models

def find_related_contacts(db: Session, email: str, phone: str):
    query = db.query(models.Contact)
    if email and phone:
        return query.filter(
            (models.Contact.email == email) | (models.Contact.phone_number == phone)
        ).all()
    elif email:
        return query.filter(models.Contact.email == email).all()
    elif phone:
        return query.filter(models.Contact.phone_number == phone).all()
    return []

def create_contact(db: Session, email: str, phone: str, linked_id=None, precedence="primary"):
    contact = models.Contact(
        email=email,
        phone_number=phone,
        linked_id=linked_id,
        link_precedence=precedence
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

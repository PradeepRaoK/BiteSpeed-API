from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database, models, schemas, crud
import os
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify(payload: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    email = payload.email
    phone = payload.phoneNumber

    related = crud.find_related_contacts(db, email, phone)

    # Case 1: no existing contact
    if not related:
        new_contact = crud.create_contact(db, email, phone)
        return {
            "contact": {
                "primaryContactId": new_contact.id,
                "emails": [email] if email else [],
                "phoneNumbers": [phone] if phone else [],
                "secondaryContactIds": []
            }
        }

    # Case 2: existing contacts
    primary_contacts = [c for c in related if c.link_precedence == "primary"]

    # ✅ FIX: handle case when all contacts are secondary (no primary found)
    if not primary_contacts:
        # Pick the oldest contact among all as new primary
        oldest = sorted(related, key=lambda x: x.created_at)[0]
        oldest.link_precedence = "primary"
        db.commit()
        db.refresh(oldest)
        primary = oldest
    else:
        primary = sorted(primary_contacts, key=lambda x: x.created_at)[0]

    secondaries = [c for c in related if c.id != primary.id]

    # Merge data sets
    emails = sorted({c.email for c in [primary] + secondaries if c.email})
    phones = sorted({c.phone_number for c in [primary] + secondaries if c.phone_number})
    secondary_ids = [c.id for c in [primary] + secondaries if c.link_precedence == "secondary"]

    # If new info not yet linked
    if (email and email not in emails) or (phone and phone not in phones):
        new_secondary = crud.create_contact(
            db, email, phone, linked_id=primary.id, precedence="secondary"
        )
        secondary_ids.append(new_secondary.id)
        if email and email not in emails:
            emails.append(email)
        if phone and phone not in phones:
            phones.append(phone)

    return {
        "contact": {
            "primaryContactId": primary.id,
            "emails": emails,
            "phoneNumbers": phones,
            "secondaryContactIds": secondary_ids
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # default 8000 locally
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

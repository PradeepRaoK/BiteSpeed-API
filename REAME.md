# Bitespeed Identify API

This FastAPI project implements the `/identify` endpoint to manage contacts with primary and secondary linking.

## Requirements

- Python 3.10+
- PostgreSQL
- pip

## Setup and Installation

```bash
git clone https://github.com/<your-username>/bitespeed.git
cd bitespeed

python -m venv venv
# Activate venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp config.example.yml config.yml    # Linux/Mac
copy config.example.yml config.yml  # Windows
# Edit config.yml to actual database url

# Initialize Database
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"

# Run the application
uvicorn bitespeed.main:app --reload

# Test API
# Request URL
http://127.0.0.1:8000/identify

# Example Response Body
{
  "email": "example@example.com",
  "phoneNumber": "1234567890"
}



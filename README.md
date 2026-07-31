# REST API Store & Integration Engine

A production-ready RESTful API service built with Python, Flask, SQLAlchemy, and Docker. Designed to simulate enterprise SaaS API behaviors, schema validations, JWT authentication flows, and relational database troubleshooting.

---

## 🚀 Tech Stack & Tools

- **Backend:** Python 3.x, Flask, Flask-RESTful
- **ORM & Database:** SQLAlchemy, SQLite (Relational Schema Modeling)
- **Data Validation:** Marshmallow (`schemas.py`)
- **Authentication & Security:** JWT Auth with active Token Revocation / Blocklist (`blocklist.py`)
- **DevOps & Containerization:** Docker, Docker Compose
- **API Spec & Testing:** OpenAPI / Swagger UI, Postman, Insomnia

---

## 🔑 Key Technical Features

- **Schema Validation & Resource Modeling:** Enforces explicit payload contracts and endpoint structures using Marshmallow schemas (`schemas.py`).
- **Relational Data Management:** Models data persistence and SQLite relational schema queries via SQLAlchemy ORM (`db.py`).
- **JWT Auth & Token Blocklisting:** Implements secure authentication flow with token revocation handling for logged-out/blacklisted sessions (`blocklist.py`).
- **Isolated Environment:** Pre-configured containerized setup using `Dockerfile` and `docker-compose.yml`.

---

## 🛠️ Quick Start

### Running with Docker (Recommended)
```bash
docker-compose up --build
```

### Local Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

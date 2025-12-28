# Tobacco Leaf Prediction API

A FastAPI-based backend for predicting tobacco leaf health using a machine learning model.
Supports user authentication (JWT), prediction history (report), and file upload.

---

## Features

- **User Authentication**

  - Register / Login / Logout
  - JWT-based token authentication

- **Prediction**

  - Upload image and get ML prediction
  - Save prediction + image path to database

- **Reports**

  - View prediction history
  - Detail & delete prediction

- **Architecture**

  - Clean repo–service pattern
  - JWT-secured routes
  - Modular routers: `predict` & `report`

---

## Project Structure

```
app/
├── api/
│   └── v1/
│       ├── auth.py
│       ├── user.py
│       ├── prediction.py
│       └── report.py
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   ├── base.py
│   └── session.py
├── models/
│   ├── user.py
│   └── prediction_report.py
├── repositories/
│   ├── user_repository.py
│   └── prediction_repository.py
├── schemas/
│   ├── auth.py
│   ├── user.py
│   └── prediction.py
├── services/
│   ├── auth_service.py
│   └── prediction_service.py
├── ml/
│   └── predictor.py
└── utils/
    └── resizer_image.py
```

---

## Requirements

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL / SQLite / MySQL (configurable)
- `python-multipart` (for file upload)
- `python-jose` (for JWT)
- Pillow / OpenCV (for image processing)
- Optional: Alembic for migrations

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/username/tobacco-prediction.git
cd tobacco-prediction
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:

```env
DATABASE_URL=sqlite:///./db.sqlite3
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Database Setup

```bash
# If using SQLite, the DB will auto-create
# For PostgreSQL/MySQL, create the DB first
# Then run migrations (if using Alembic)
alembic upgrade head
```

---

## Run Development Server

```bash
uvicorn app.main:app --reload
```

Open Swagger docs at: `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Auth

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | `/auth/register` | Register user           |
| POST   | `/auth/login`    | Login and get JWT token |

### User

| Method | Endpoint | Description             |
| ------ | -------- | ----------------------- |
| GET    | `/user/` | List users (admin only) |

### Prediction

| Method | Endpoint            | Description                                |
| ------ | ------------------- | ------------------------------------------ |
| POST   | `/predictions/`     | Upload image & predict                     |
| GET    | `/predictions/`     | List user predictions (optional if needed) |
| GET    | `/predictions/{id}` | Detail of a prediction                     |
| DELETE | `/predictions/{id}` | Delete a prediction                        |

### Reports

| Method | Endpoint        | Description                  |
| ------ | --------------- | ---------------------------- |
| GET    | `/reports/`     | List user prediction reports |
| GET    | `/reports/{id}` | Get single report            |
| DELETE | `/reports/{id}` | Delete a report              |

> All endpoints (except `/auth/register` & `/auth/login`) require `Authorization: Bearer <token>` header.

---

## Security

- JWT authentication
- All actions tied to `user_id` from token
- Users cannot access or delete other users’ predictions

---

## Testing

Use **Postman / Insomnia / Swagger UI** to test:

- Register user
- Login & get token
- Upload image to `/predictions`
- Fetch reports from `/reports`

---

## Notes

- Images are resized & saved via `utils/resizer_image.py`
- Prediction logic is in `ml/predictor.py`
- Pagination, filtering, and admin access can be added later

---

## Dependencies

```text
fastapi
uvicorn
sqlalchemy
pydantic
python-multipart
python-jose
passlib
pillow
```

---

## License

MIT License

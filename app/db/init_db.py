from app.db.session import engine
from app.db.base import Base

# import semua model agar dikenali SQLAlchemy
from app.models import user

def init_db():
    Base.metadata.create_all(bind=engine)

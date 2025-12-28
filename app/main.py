from fastapi import FastAPI
from app.api.v1 import user
from app.api.v1 import auth
from app.api.v1 import prediction
from app.db.init_db import init_db

app = FastAPI(title='My me')

@app.on_event('startup')
def startup():
    init_db()


app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router,prefix = "/api/v1")
app.include_router(prediction.router, prefix = "/api/v1")
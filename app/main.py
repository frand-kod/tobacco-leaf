from fastapi import FastAPI
from app.api.v1 import user,auth,prediction,report
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db

from fastapi.staticfiles import StaticFiles

app = FastAPI(title='My me')

@app.on_event('startup')
def startup():
    init_db()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router,prefix = "/api/v1")
app.include_router(prediction.router, prefix = "/api/v1")
app.include_router(report.router,prefix = "/api/v1")

# static folder
app.mount("/uploads",StaticFiles(directory="app/uploads"),name='uploads')
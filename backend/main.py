from fastapi import FastAPI
from app.routes import upload, analyze, negotiate, vin

from app.models.contract import Contract


from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Car Contract AI")

app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(negotiate.router)
app.include_router(vin.router)

@app.get("/")
def root():
    return {"status": "Car Contract AI running"}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

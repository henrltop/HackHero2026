from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine, Base
import app.models  # noqa: F401 — registra todos os modelos antes de criar tabelas

from app.api.auth import router as auth_router
from app.api.analyze import router as analyze_router
from app.api.alerts import router as alerts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Vigília API", version="0.1.0", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(analyze_router)
app.include_router(alerts_router)


@app.get("/health")
def health():
    return {"status": "ok"}

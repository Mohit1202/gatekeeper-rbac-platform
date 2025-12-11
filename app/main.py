from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import auth, user, task
from app.db.session import engine, Base
from app.core.config import settings
from app.core.logging_config import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/checked successfully")
        yield
    finally:
        logger.info("Application shutdown complete")


app = FastAPI(
    title="Gatekeeper RBAC Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}

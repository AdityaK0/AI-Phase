from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
from app.exceptions import AppException, app_exception_handler
from app.middleware import DBSessionMiddleware
from app.users.api import router as users_router

create_tables()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.APP_DEBUG,
)

# DBSessionMiddleware must come first — it sets up the session ContextVar
# that every repository depends on for the lifetime of the request
app.add_middleware(DBSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)

# ── routes ────────────────────────────────────────────────────────────────────
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
# app.include_router(products_router, prefix="/api/v1/products", tags=["products"])


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

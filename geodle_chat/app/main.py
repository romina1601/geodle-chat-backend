from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from geodle_chat.api.endpoints import router
from geodle_chat.core.config import settings

app = FastAPI(title="Geodle Chat Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoint routers
app.include_router(router)


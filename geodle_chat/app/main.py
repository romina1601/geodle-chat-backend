from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from geodle_chat.api.endpoints import router

app = FastAPI(title="Geodle Chat Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # TODO: Adjust this after deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoint routers
app.include_router(router)


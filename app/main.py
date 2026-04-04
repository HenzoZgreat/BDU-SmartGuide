from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ask import router as ask_router

app = FastAPI()

# 🔹 Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allows requests from ANY origin
    allow_credentials=False,    # ⚠️ Must be False when using "*"
    allow_methods=["*"],        # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],        # Allows custom headers (Content-Type, Authorization, etc.)
)

app.include_router(ask_router)
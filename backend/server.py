"""Backend API server — FastAPI app with photo upload and auth."""

import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import BACKEND_PORT, PHOTOS_DIR
from backend.auth.routes import router as auth_router
from backend.photos.routes import router as photos_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

app = FastAPI(title="Yael Englander Backend", version="1.0.0")

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://www.yaelenglander.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files — serve photos
app.mount("/files/photos", StaticFiles(directory=str(PHOTOS_DIR)), name="photos")

# Routes
app.include_router(auth_router)
app.include_router(photos_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "backend-api"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)

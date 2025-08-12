"""FastAPI application for Utah River Lake Data API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import rivers, lakes

app = FastAPI(
    title="Utah River Lake Data API",
    description="API for retrieving Utah river and lake level data from USGS",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rivers.router, prefix="/api/v1/rivers", tags=["rivers"])
app.include_router(lakes.router, prefix="/api/v1/lakes", tags=["lakes"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Utah River Lake Data API"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
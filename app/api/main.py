from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api import auth, proteins
from app.core.rate_limiter import limiter

app = FastAPI(
    title="Protein Lab API",
    description="Comprehensive protein database management API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(proteins.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Protein Lab API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

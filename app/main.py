from fastapi import FastAPI
from .api import router

app = FastAPI(
    title="Sparse Embedding Server",
    description="API for generating sparse embeddings using embed-anything.",
    version="1.0.0"
)

app.include_router(router)

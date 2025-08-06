from fastapi import APIRouter, Request, HTTPException
from .model import compute_sparse_embedding

router = APIRouter()

@router.post("/embed")
async def embed(request: Request):
    """
    Accepts a JSON payload: {"texts": ["..."]}
    Returns: {"indices": [...], "vecs": [...]}
    """
    try:
        data = await request.json()
        texts = data.get("texts")
        if not texts or not isinstance(texts, list):
            raise HTTPException(status_code=400, detail="Missing or invalid 'texts' in request body")
        indices, vecs = compute_sparse_embedding(texts)
        return {"indices": indices, "vecs": vecs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {str(e)}")

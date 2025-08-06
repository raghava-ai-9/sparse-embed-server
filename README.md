# Sparse Embedding Server

A lightweight FastAPI server for generating sparse embeddings using the [embed-anything](https://github.com/prithivida/embed-anything) package and the `prithivida/Splade_PP_en_v1` model. Designed for use as a microservice for RAG pipelines and Qdrant hybrid search.

## Features

- Exposes a `/embed` API endpoint for sparse embedding generation.
- Loads the SPLADE sparse model at startup.
- Returns embeddings in a format compatible with Qdrant's sparse vector ingestion.

## Project Structure

```
sparse-embed-server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   └── api.py
├── requirements.txt
├── README.md
```

## Installation

1. Clone this repo or copy the folder.
2. Install dependencies (Python 3.8+ recommended):

   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8130
```

## API Usage

### POST `/embed`

**Request:**
```json
{
  "text": "Your text to embed"
}
```

**Response:**
```json
{
  "embedding": {
    "token_id_1": weight1,
    "token_id_2": weight2,
    ...
  }
}
```

- The `embedding` is a dictionary mapping token IDs to their weights (sparse vector).

**Example with curl:**
```bash
curl -X POST "http://localhost:8130/embed" -H "Content-Type: application/json" -d '{"text": "hello world"}'
```

## Python Client Example

```python
import requests

def compute_vectors(text, server_url="http://localhost:8130/embed"):
    response = requests.post(server_url, json={"text": text})
    response.raise_for_status()
    return response.json()["embedding"]
```

## Notes

- The model is loaded at server startup for efficiency.
- For production, consider using a process manager and enabling CORS if needed.

## License

MIT

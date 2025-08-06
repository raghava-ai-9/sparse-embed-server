import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer
from typing import List, Tuple

model_id = "prithivida/Splade_PP_en_v1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForMaskedLM.from_pretrained(model_id)

def compute_sparse_embedding(texts: List[str]) -> Tuple[List[List[int]], List[List[float]]]:
    """
    Computes sparse vectors for a list of texts.
    Returns a tuple (indices, vecs), where each is a list of lists:
      - indices: list of nonzero token indices for each text
      - vecs: list of corresponding values for each text
    """
    if isinstance(texts, str):
        texts = [texts]
    tokens = tokenizer(
        texts, truncation=True, padding=True, max_length=512, return_tensors="pt"
    )
    if torch.cuda.is_available():
        model.to("cuda")
        tokens = {k: v.to("cuda") for k, v in tokens.items()}

    with torch.no_grad():
        output = model(**tokens)
        logits, attention_mask = output.logits, tokens["attention_mask"]
        relu_log = torch.log(1 + torch.relu(logits))
        weighted_log = relu_log * attention_mask.unsqueeze(-1)
        tvecs, _ = torch.max(weighted_log, dim=1)

        indices = []
        vecs = []
        for batch in tvecs:
            idx = batch.nonzero(as_tuple=True)[0].tolist()
            indices.append(idx)
            vecs.append([batch[i].item() for i in idx])

        return indices, vecs

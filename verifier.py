"""
verifier.py

Verifies claims against retrieved evidence using a pretrained NLI
(Natural Language Inference) model. For each (evidence, claim) pair, the
model outputs one of: entailment, contradiction, or neutral, with a
confidence score.

This is the "does the evidence actually support the claim" stage — sitting
between evidence retrieval and hallucination detection.
"""

from typing import Dict, List

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from config import NLI_CONFIDENCE_THRESHOLD, NLI_MODEL_NAME

_tokenizer = AutoTokenizer.from_pretrained(NLI_MODEL_NAME)
_model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL_NAME)
_model.eval()

# roberta-large-mnli label order: 0 = contradiction, 1 = neutral, 2 = entailment
_LABELS = ["contradiction", "neutral", "entailment"]


def verify_claim_against_evidence(evidence_text: str, claim_text: str) -> Dict:
    """
    Run NLI on a single (evidence, claim) pair.

    NLI convention: premise = evidence, hypothesis = claim.
    "Does the evidence entail/contradict/say nothing about the claim?"

    Returns:
        {
            "label": "entailment" | "neutral" | "contradiction",
            "confidence": float,   # confidence in the predicted label
            "scores": {"entailment": float, "neutral": float, "contradiction": float}
        }
    """
    inputs = _tokenizer(evidence_text, claim_text, return_tensors="pt", truncation=True)

    with torch.no_grad():
        logits = _model(**inputs).logits

    probs = torch.softmax(logits, dim=1)[0]
    scores = {label: float(probs[i]) for i, label in enumerate(_LABELS)}

    predicted_idx = int(torch.argmax(probs))
    predicted_label = _LABELS[predicted_idx]
    confidence = scores[predicted_label]

    # If the model isn't confident enough, treat it as neutral/uncertain
    # rather than trusting a low-confidence entailment/contradiction call.
    if confidence < NLI_CONFIDENCE_THRESHOLD and predicted_label != "neutral":
        predicted_label = "neutral"

    return {
        "label": predicted_label,
        "confidence": confidence,
        "scores": scores,
    }


def verify_claim(claim_text: str, evidence_list: List[Dict]) -> Dict:
    """
    Verify a claim against a list of retrieved evidence items (as produced
    by evidence_retriever.retrieve_evidence).

    Runs NLI against each evidence item and aggregates:
      - If any evidence entails the claim -> overall "entailment"
      - Else if any evidence contradicts the claim -> overall "contradiction"
      - Else -> "neutral" (includes the case of no evidence at all)

    Returns:
        {
            "claim": str,
            "label": "entailment" | "contradiction" | "neutral",
            "best_match": {evidence dict + nli result} or None,
            "all_results": [ {evidence dict + nli result}, ... ]
        }
    """
    if not evidence_list:
        return {
            "claim": claim_text,
            "label": "neutral",
            "best_match": None,
            "all_results": [],
        }

    all_results = []
    for evidence in evidence_list:
        nli_result = verify_claim_against_evidence(evidence["text"], claim_text)
        all_results.append({**evidence, **nli_result})

    entailments = [r for r in all_results if r["label"] == "entailment"]
    contradictions = [r for r in all_results if r["label"] == "contradiction"]

    if entailments:
        overall_label = "entailment"
        best_match = max(entailments, key=lambda r: r["confidence"])
    elif contradictions:
        overall_label = "contradiction"
        best_match = max(contradictions, key=lambda r: r["confidence"])
    else:
        overall_label = "neutral"
        best_match = max(all_results, key=lambda r: r["confidence"])

    return {
        "claim": claim_text,
        "label": overall_label,
        "best_match": best_match,
        "all_results": all_results,
    }


if __name__ == "__main__":
    from evidence_retriever import retrieve_evidence

    test_claims = [
        "India became independent in 1947.",
        "Jawaharlal Nehru was the first Prime Minister of India.",
        "India became independent in 1950.",  # subtly wrong -> should contradict
        "The Eiffel Tower is located in Rome.",  # no evidence -> neutral
    ]

    for claim in test_claims:
        evidence = retrieve_evidence(claim)
        result = verify_claim(claim, evidence)

        print(f"\nClaim: {result['claim']}")
        print(f"Overall label: {result['label']}")
        if result["best_match"]:
            bm = result["best_match"]
            print(f"  Best match: [{bm['label']}, conf={bm['confidence']:.3f}] {bm['text']}")
        else:
            print("  No evidence available.")
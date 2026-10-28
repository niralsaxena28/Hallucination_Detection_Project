"""
claim_extractor.py

Splits an LLM response into individual sentences/claims and extracts named
entities from each, so downstream modules (evidence retrieval, NLI
verification) get structured, filtered claims instead of raw sentences.
"""

import re
from typing import Dict, List

import spacy

nlp = spacy.load("en_core_web_sm")

# Sentences shorter than this (in characters) are usually fragments,
# greetings, or filler ("Sure!", "Okay.") rather than factual claims.
MIN_CLAIM_LENGTH = 8

# Conversational openers / filler that shouldn't be treated as factual claims.
_FILLER_PATTERNS = [
    r"^(sure|okay|ok|certainly|of course|great question)[!.,]?$",
    r"^(here('|’)s|here is|let me|i('|’)?ll|i can)\b",
]


def _is_likely_claim(sentence: str) -> bool:
    """Filter out sentences that aren't worth fact-checking: questions,
    very short fragments, and common filler/greetings."""
    text = sentence.strip()

    if len(text) < MIN_CLAIM_LENGTH:
        return False

    if text.endswith("?"):
        return False

    lowered = text.lower()
    for pattern in _FILLER_PATTERNS:
        if re.match(pattern, lowered):
            return False

    return True


def extract_claims(text: str) -> List[str]:
    """
    Split an LLM response into individual sentences/claims.

    Kept for backward compatibility with existing code (e.g. main.py):
    returns a plain list of claim strings, filtered and cleaned.
    """
    return [c["text"] for c in extract_claims_detailed(text)]


def extract_claims_detailed(text: str) -> List[Dict]:
    """
    Split an LLM response into individual claims, filtering out
    non-factual sentences (questions, greetings, fragments), and attach
    named entities to each remaining claim.

    Returns a list of dicts:
        {
            "id": int,
            "text": str,
            "entities": [{"text": str, "label": str}, ...]
        }
    """
    if not text or not text.strip():
        return []

    doc = nlp(text)
    claims = []
    claim_id = 0

    for sentence in doc.sents:
        sentence_text = sentence.text.strip()

        if not sentence_text or not _is_likely_claim(sentence_text):
            continue

        entities = [{"text": ent.text, "label": ent.label_} for ent in sentence.ents]

        claims.append(
            {
                "id": claim_id,
                "text": sentence_text,
                "entities": entities,
            }
        )
        claim_id += 1

    return claims


if __name__ == "__main__":
    sample_text = (
        "Sure, here's what I found. "
        "India became independent in 1947. "
        "Jawaharlal Nehru was the first Prime Minister of India. "
        "Is that helpful? "
        "Albert Einstein was born in Germany in 1879."
    )

    print("Simple claims (backward-compatible):")
    for c in extract_claims(sample_text):
        print(f"  - {c}")

    print("\nDetailed claims with entities:")
    for c in extract_claims_detailed(sample_text):
        print(f"  [{c['id']}] {c['text']}")
        for ent in c["entities"]:
            print(f"      -> {ent['text']} ({ent['label']})")

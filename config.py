import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_DATA_PATH = os.path.join(BASE_DIR, "evidence_data.json")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

EVIDENCE_SIMILARITY_THRESHOLD = 0.55

EVIDENCE_TOP_K = 3

SPACY_MODEL_NAME = "en_core_web_sm"

MIN_CLAIM_LENGTH = 8

NLI_MODEL_NAME = "roberta-large-mnli"

NLI_CONFIDENCE_THRESHOLD = 0.6

FINAL_CONFIDENCE_THRESHOLD = 0.5

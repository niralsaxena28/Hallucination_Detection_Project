
"""
main.py

Current pipeline stage: Claim Extraction -> Evidence Retrieval.
(Verification / NLI / hallucination detection / correction come next.)
"""

from claim_extractor import extract_claims_detailed
from evidence_retriever import retrieve_evidence


def run_pipeline(llm_response: str):
    claims = extract_claims_detailed(llm_response)

    if not claims:
        print("No factual claims were found in the response.")
        return

    print(f"Extracted {len(claims)} claim(s):\n")

    for claim in claims:
        print(f"{claim['id'] + 1}. {claim['text']}")

        if claim["entities"]:
            entity_str = ", ".join(f"{e['text']} ({e['label']})" for e in claim["entities"])
            print(f"   Entities: {entity_str}")
        else:
            print("   Entities: none detected")

        evidence = retrieve_evidence(claim["text"])

        if not evidence:
            print("   Evidence: none found (unverifiable / possible hallucination)")
        else:
            print("   Evidence:")
            for e in evidence:
                print(f"     - [{e['score']:.3f}] {e['text']}  (source: {e['source']})")

        print()


if __name__ == "__main__":
    response = """
    India became independent in 1947.
    Jawaharlal Nehru was the first Prime Minister of India.
    The Eiffel Tower is located in Rome.
    """

    run_pipeline(response)

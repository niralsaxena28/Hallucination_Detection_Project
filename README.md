# Verity AI — Hallucination Detection, Verification & Correction Framework

An AI-powered framework that analyses AI-generated responses, extracts factual claims, retrieves supporting evidence, detects potential hallucinations, and generates corrected responses with transparent verification results.

## Overview 

Large Language Models (LLMs) can generate convincing answers containing inaccurate or unsupported information. **Verity AI** aims to address this challenge through claim-level verification, evidence retrieval, and automated correction.

The project provides an interactive Streamlit dashboard where users can submit a response and inspect the verification results, evidence, confidence estimates, and corrected output.

## Key Features

- **Claim Extraction:** Identifies individual factual claims from an AI-generated response.
- **Evidence Retrieval:** Searches a local evidence database for relevant information using semantic similarity.
- **Claim Verification:** Classifies claims as supported, contradicted, or unverified based on the existing verification pipeline.
- **Hallucination Detection:** Highlights claims that conflict with retrieved evidence.
- **Response Correction:** Attempts to correct contradicted or inaccurate claims using available evidence.
- **Explainable Results:** Presents claim-level decisions and supporting evidence.
- **Interactive Dashboard:** Provides an interface for running analyses and reviewing results.
- **Visual Analytics:** Displays verification statistics and a distribution of claim classifications.
- **Downloadable Output:** Allows users to download the corrected response.
- **Theme Support:** Includes dark and light appearance options.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and AI pipeline |
| Streamlit | Interactive dashboard |
| Sentence Transformers | Semantic text embeddings |
| FAISS | Similarity-based evidence retrieval |
| spaCy | Natural language processing and entity analysis |
| PyTorch | Machine learning model support |
| JSON | Local evidence storage |
| Pandas / Plotting libraries | Data handling and visualisation, where used |

## Project Structure

```text
Hallucination_Detection_Project/
│
├── app.py                  # Streamlit dashboard
├── main.py                 # Main verification pipeline
├── claim_extractor.py      # Factual claim extraction
├── evidence_retriever.py   # Evidence retrieval and similarity search
├── verifier.py             # Claim verification
├── corrector.py            # Response correction
├── config.py               # Configuration settings
├── utils.py                # Utility functions, if included
├── evidence_data.json      # Local evidence database
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
└── data/                   # Additional data, if used
```

*The structure above is illustrative. Keep only the files and folders that actually exist in your repository.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Hallucination_Detection_Project
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

If your project contains a `requirements.txt` file:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a dependency is missing, install it according to your project's actual requirements.

### 4. Download the spaCy language model

If your application uses `en_core_web_sm`, run:

```bash
python -m spacy download en_core_web_sm
```

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser to access the dashboard.

## How It Works

The framework follows a multi-stage verification process:

1. **Input:** The user submits an AI-generated response.
2. **Claim extraction:** The response is divided into individual factual claims.
3. **Evidence retrieval:** The system searches the local evidence database for relevant passages.
4. **Verification:** The existing verification logic evaluates the claims against retrieved evidence.
5. **Classification:** Claims are categorised as supported, contradicted, or unverified.
6. **Correction:** The correction module attempts to revise claims that are contradicted or inaccurate.
7. **Output:** The dashboard displays claim-level results, evidence, summary statistics, and the corrected response.

## Example

**Input response:**

> India became independent in 1947. India became a republic in 1955. The capital of India is New Delhi.

**Expected verification behaviour:**

- India's independence in 1947 — Supported.
- India's becoming a republic in 1955 — Contradicted by evidence that the Constitution came into effect on 26 January 1950.
- New Delhi as India's capital — Supported.

The actual output depends on the evidence available in the database and the behaviour of the verification pipeline.

## Important Limitations

- Verification quality depends on the coverage and accuracy of the available evidence.
- Missing evidence can result in an unverified claim, even when the claim is true.
- Semantic similarity does not independently establish factual correctness.
- Confidence scores are model estimates, not guarantees of truth.
- Automated corrections should be reviewed, particularly for high-impact applications.
- The framework should not be treated as a substitute for authoritative fact-checking.

## Future Enhancements

- Integration with trusted external knowledge sources.
- Expanded evidence coverage and source-quality assessment.
- Improved contradiction detection using Natural Language Inference (NLI).
- Source citations and evidence provenance for every claim.
- Evaluation against labelled hallucination-detection datasets.
- Performance metrics such as precision, recall, F1-score, and verification accuracy.
- Improved reporting and export functionality.

## Academic Project

Developed as a B.Tech Computer Science and Engineering project specialising in Artificial Intelligence and Machine Learning.

**Project:** Hallucination Detection, Verification and Correction Framework  
**Interface:** Verity AI Research Workbench  
**Developer:** Niral Saxena

## Disclaimer

This project is intended for educational and research purposes. Verification and correction results depend on the underlying models, evidence sources, and implementation.


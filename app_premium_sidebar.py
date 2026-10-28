"""Premium Streamlit UI for the existing hallucination-detection pipeline.
Run from the project root: streamlit run app.py
"""
import html
import pandas as pd
import streamlit as st

from config import STATUS_HALLUCINATED, STATUS_SUPPORTED, STATUS_UNVERIFIED
from main import analyze_response

st.set_page_config(page_title="Verity AI | Research Workbench", page_icon="🔎", layout="wide")

DEMO_TEXT = (
    "India became independent in 1947.\n"
    "Jawaharlal Nehru was the first Prime Minister of India.\n"
    "India became a republic in 1955.\n"
    "The capital of India is New Delhi."
)


def init_state():
    defaults = {
        "response_input": "",
        "analysis_result": None,
        "analysis_input": "",
        "theme_mode": "Dark",
        "active_view": "Overview",
        "analysis_error": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_demo():
    st.session_state.response_input = DEMO_TEXT
    st.session_state.analysis_result = None
    st.session_state.analysis_input = ""
    st.session_state.analysis_error = ""


def clear_workspace():
    st.session_state.response_input = ""
    st.session_state.analysis_result = None
    st.session_state.analysis_input = ""
    st.session_state.analysis_error = ""


def run_analysis():
    text = st.session_state.response_input
    if not text or not text.strip():
        st.session_state.analysis_error = "Please enter a response before analysing."
        st.session_state.analysis_result = None
        return
    try:
        st.session_state.analysis_error = ""
        with st.spinner("Extracting claims, retrieving evidence and running verification…"):
            # Use the real existing pipeline; no simulated verdicts.
            result = analyze_response(text)
        st.session_state.analysis_result = result
        st.session_state.analysis_input = text
    except Exception as exc:
        st.session_state.analysis_result = None
        st.session_state.analysis_error = "Analysis failed. Check the VS Code terminal for details."
        print(f"Analysis error: {type(exc).__name__}: {exc}")


def inject_css(theme):
    dark = theme == "Dark"
    c = {
        "bg": "#0B1020" if dark else "#F3F6FC",
        "panel": "#111A2E" if dark else "#FFFFFF",
        "text": "#E8EEF8" if dark else "#172033",
        "muted": "#9BAAC2" if dark else "#65728A",
        "border": "#26344D" if dark else "#DCE4EF",
        "accent": "#8B9CFF" if dark else "#4F46E5",
        "input": "#0E1729" if dark else "#FFFFFF",
    }
    st.markdown(f"""
    <style>
    .stApp {{background:{c['bg']}; color:{c['text']};}}
    [data-testid="stHeader"] {{background:transparent;}}
    [data-testid="stSidebar"] {{background:{c['panel']};border-right:1px solid {c['border']};}}
    [data-testid="stSidebar"] * {{color:{c['text']};}}
    [data-testid="stSidebar"] > div {{
        padding: 1.4rem 1.15rem 2rem;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {{
        font-size: 1.42rem;
        letter-spacing: -.035em;
        line-height: 1.25;
        margin-top: .35rem;
        margin-bottom: .55rem;
    }}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        font-size: .88rem;
        line-height: 1.6;
    }}
    [data-testid="stSidebar"] hr {{
        margin: 1.25rem 0;
        opacity: .65;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] {{
        gap: .5rem;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] label {{
        border-radius: 10px;
        padding: .32rem .48rem;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        line-height: 1.65;
    }}
    .brand-mark {{
        display: inline-flex;
        width: 2.7rem;
        height: 2.7rem;
        align-items: center;
        justify-content: center;
        border-radius: 13px;
        margin-bottom: .9rem;
        background: {c['accent']};
        color: #FFFFFF !important;
        font-size: 1.2rem;
        font-weight: 900;
        box-shadow: 0 8px 22px {c['accent']}33;
    }}
    .sidebar-tagline {{
        color: {c['muted']} !important;
        font-size: .87rem;
        line-height: 1.65;
    }}
    .block-container {{max-width:1560px;padding-top:1.8rem;padding-bottom:3.2rem;}}
    h1,h2,h3,h4,p,label,.stMarkdown {{color:{c['text']};}}
    .eyebrow {{color:{c['accent']}!important;font-size:.76rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;}}
    .hero-title {{font-size:clamp(1.9rem,3vw,2.7rem);line-height:1.12;font-weight:850;letter-spacing:-.04em;margin:.25rem 0;}}
    .subtitle {{color:{c['muted']}!important;margin:.6rem 0 1.4rem;font-size:1rem;}}
    .surface {{background:{c['panel']};border:1px solid {c['border']};border-radius:16px;padding:1.05rem 1.15rem;}}
    .metric-label {{color:{c['muted']}!important;font-size:.82rem;font-weight:650;margin-bottom:.45rem;}}
    .metric-value {{color:{c['text']}!important;font-size:1.8rem;font-weight:800;line-height:1.1;overflow-wrap:anywhere;}}
    .metric-foot {{color:{c['muted']}!important;font-size:.77rem;margin-top:.45rem;}}
    div[data-testid="stTextArea"] textarea {{background:{c['input']};color:{c['text']};border:1px solid {c['border']};border-radius:12px;}}
    div[data-testid="stExpander"] {{background:{c['panel']};border:1px solid {c['border']};border-radius:12px;}}
    div[data-testid="stMetric"] {{background:{c['panel']};border:1px solid {c['border']};padding:.8rem;border-radius:12px;min-width:0;}}
    .stButton>button {{border-radius:10px;min-height:2.6rem;font-weight:700;border:1px solid {c['border']};}}
    .stButton>button[kind="primary"] {{background:{c['accent']};border-color:{c['accent']};color:white;}}
    hr {{border-color:{c['border']};}}
    </style>
    """, unsafe_allow_html=True)


def metric_card(label, value, foot):
    st.markdown(
        f'<div class="surface"><div class="metric-label">{html.escape(str(label))}</div>'
        f'<div class="metric-value">{html.escape(str(value))}</div>'
        f'<div class="metric-foot">{html.escape(str(foot))}</div></div>',
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="brand-mark">V</div><div class="eyebrow">VERITY AI · LAB</div>',
            unsafe_allow_html=True,
        )
        st.markdown("## Research Workbench")
        st.markdown(
            '<div class="sidebar-tagline">Claim-level fact checking, evidence tracing, and transparent AI verification.</div>',
            unsafe_allow_html=True,
        )
        st.divider()
        st.radio(
            "Workspace",
            ["Overview", "Claim analysis", "Evidence & sources", "Pipeline"],
            key="active_view",
        )
        st.divider()
        st.markdown("**Appearance**")
        st.radio("Theme", ["Dark", "Light"], key="theme_mode", horizontal=True)
        st.divider()
        st.markdown("**Verification stack**")
        st.caption("Claim extraction · spaCy NER · Sentence Transformers · FAISS · NLI")
        st.caption("Results shown here come from your Python pipeline.")


def fmt_num(value, digits=3):
    try:
        return f"{float(value):.{digits}f}" if value is not None else "N/A"
    except (TypeError, ValueError):
        return "N/A"


def fmt_pct(value):
    try:
        return f"{float(value):.1%}" if value is not None else "N/A"
    except (TypeError, ValueError):
        return "N/A"


def status_icon(status):
    if status == STATUS_SUPPORTED:
        return "🟢"
    if status == STATUS_HALLUCINATED:
        return "🔴"
    if status == STATUS_UNVERIFIED:
        return "🟡"
    return "⚪"


def render_summary(result):
    claims = result.get("claims") or []
    summary = result.get("summary") or {}
    total = summary.get("total_claims", len(claims))
    supported = summary.get("supported", 0)
    contradicted = summary.get("hallucinated", 0)
    unverified = summary.get("unverified", 0)

    # Two columns per row avoid overflowing the viewport on narrower screens.
    row1 = st.columns(2, gap="small")
    row2 = st.columns(2, gap="small")
    items = [
        ("Claims analysed", total, "Factual claims extracted"),
        ("Supported", supported, "Evidence supports claim"),
        ("Contradicted", contradicted, "Classified as contradicted"),
        ("Unverified", unverified, "Evidence inconclusive or unavailable"),
    ]
    for col, item in zip(row1 + row2, items):
        with col:
            metric_card(*item)

    st.write("")
    left, right = st.columns([1.2, 1], gap="large")
    with left:
        st.markdown("### Verification distribution")
        if total:
            df = pd.DataFrame({
                "Status": ["Supported", "Contradicted", "Unverified"],
                "Claims": [supported, contradicted, unverified],
            })
            st.bar_chart(df.set_index("Status"), height=280, horizontal=True)
        else:
            st.info("No factual claims were returned by the extractor.")
    with right:
        st.markdown("### Confidence overview")
        metric_card(
            "Average model confidence",
            fmt_pct(summary.get("average_confidence")),
            "A model estimate, not proof of truth",
        )


def render_claims(claims):
    if not claims:
        st.info("No factual claims were detected in this response.")
        return

    for claim in claims:
        claim_id = claim.get("claim_id", "?")
        claim_text = claim.get("text", "(claim text unavailable)")
        status = claim.get("status", STATUS_UNVERIFIED)
        with st.expander(f"{status_icon(status)} [{claim_id}] {claim_text} · {status}"):
            st.markdown("**Claim**")
            st.write(claim_text)

            a, b, c = st.columns(3)
            a.metric("Status", status)
            b.metric("Semantic similarity", fmt_num(claim.get("similarity")))
            c.metric("Model confidence", fmt_pct(claim.get("confidence")))

            nli_label = claim.get("nli_label") or "N/A"
            st.markdown(
                f"**NLI result:** {nli_label} · confidence "
                f"{fmt_num(claim.get('nli_confidence'))}"
            )
            if claim.get("reason"):
                st.markdown("**Explanation**")
                st.write(claim["reason"])

            st.markdown("**Detected entities (spaCy NER)**")
            entities = claim.get("entities") or []
            if entities:
                entity_rows = [
                    {"Entity": item.get("text", ""), "Label": item.get("label", "")}
                    for item in entities
                ]
                st.dataframe(
                    pd.DataFrame(entity_rows),
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.caption("No entities were returned for this claim.")

            st.markdown("**Evidence used**")
            evidence = claim.get("evidence_text")
            if evidence:
                st.info(evidence)
                if claim.get("evidence_source"):
                    st.caption(f"Source: {claim['evidence_source']}")
                if claim.get("evidence_url"):
                    st.markdown(f"[Open evidence source]({claim['evidence_url']})")
            else:
                st.warning(
                    "No relevant evidence was returned. Missing evidence alone "
                    "does not prove a claim false."
                )

            if claim.get("corrected_text"):
                st.markdown("**Claim-level correction**")
                st.write(claim["corrected_text"])


def render_evidence(claims):
    rows = []
    for claim in claims:
        if claim.get("evidence_text"):
            rows.append({
                "Claim ID": claim.get("claim_id", ""),
                "Claim": claim.get("text", ""),
                "Status": claim.get("status", STATUS_UNVERIFIED),
                "Evidence": claim["evidence_text"],
                "Source": claim.get("evidence_source") or "Not specified",
                "URL": claim.get("evidence_url") or "",
            })

    if not rows:
        st.info("No evidence passages or source references were returned.")
        st.caption("Evidence coverage is a retrieval limitation, not a verdict.")
        return

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
        column_config={
            "URL": st.column_config.LinkColumn("Source URL", display_text="Open source"),
            "Evidence": st.column_config.TextColumn("Evidence passage", width="large"),
            "Claim": st.column_config.TextColumn("Claim", width="large"),
        },
    )


def render_pipeline():
    stages = [
        ("01", "Response input", "Text supplied by the user"),
        ("02", "Claim extraction", "Extract factual claims"),
        ("03", "Entity analysis", "spaCy named entity recognition"),
        ("04", "Evidence retrieval", "Sentence Transformers + FAISS and configured sources"),
        ("05", "NLI verification", "Compare each claim with retrieved evidence"),
        ("06", "Classification", "Supported, contradicted, or unverified"),
        ("07", "Correction", "Build response using existing pipeline output"),
        ("08", "Explainability", "Reasons, confidence, evidence, and sources"),
    ]
    for number, title, description in stages:
        st.markdown(
            f'<div class="surface" style="margin-bottom:.65rem;display:flex;gap:1rem;">'
            f'<div style="font-weight:800;color:#8B9CFF;min-width:2rem;">{number}</div>'
            f'<div><b>{title}</b><br><span style="opacity:.75;">{description}</span></div></div>',
            unsafe_allow_html=True,
        )


def main():
    init_state()
    inject_css(st.session_state.theme_mode)
    render_sidebar()

    st.markdown('<div class="eyebrow">AI RESEARCH / FACT VERIFICATION</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">Hallucination Detection<br>Research Workbench</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">Inspect factual claims, trace evidence, and understand '
        'verification decisions — without hiding uncertainty.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("### Analyse a response")
        st.caption("Paste an LLM-generated response or load the included demo.")
        st.text_area(
            "Response text",
            key="response_input",
            height=170,
            placeholder="Paste the response you want to verify…",
            label_visibility="collapsed",
        )
        c1, c2, c3, _ = st.columns([1.2, 1, 1.1, 2.2])
        with c1:
            st.button("Run analysis", type="primary", use_container_width=True, on_click=run_analysis)
        with c2:
            st.button("Load demo", use_container_width=True, on_click=load_demo)
        with c3:
            st.button("Clear workspace", use_container_width=True, on_click=clear_workspace)

    if st.session_state.analysis_error:
        st.error(st.session_state.analysis_error)

    result = st.session_state.analysis_result
    if not result:
        st.markdown(
            '<div class="surface"><div class="eyebrow">READY FOR ANALYSIS</div>'
            '<h3>Your research workspace is ready</h3>'
            '<p>Run an analysis to view claim-level verdicts, retrieved evidence, '
            'confidence estimates, explainability, and the corrected response.</p></div>',
            unsafe_allow_html=True,
        )
        return

    claims = result.get("claims") or []
    st.divider()
    st.markdown("### Analysis results")
    st.caption(
        f"{len(claims)} claim(s) returned by the existing Python pipeline. "
        "Verdicts are not simulated."
    )

    view = st.session_state.active_view
    if view == "Overview":
        render_summary(result)
        st.markdown("### Claim-by-claim results")
        render_claims(claims)
    elif view == "Claim analysis":
        st.markdown("### Explainability and claim inspection")
        render_claims(claims)
    elif view == "Evidence & sources":
        st.markdown("### Retrieved evidence and sources")
        render_evidence(claims)
    elif view == "Pipeline":
        st.markdown("### Verification pipeline")
        render_pipeline()

    st.divider()
    st.markdown("### Corrected response")
    corrected = result.get("corrected_response")
    if corrected:
        st.markdown(
            f'<div class="surface" style="white-space:pre-wrap;">{html.escape(str(corrected))}</div>',
            unsafe_allow_html=True,
        )
        st.download_button(
            "Download corrected response",
            data=str(corrected),
            file_name="corrected_response.txt",
            mime="text/plain",
        )
    else:
        st.info("The pipeline did not return a corrected response.")

    with st.expander("Show raw pipeline result (debug)"):
        st.json(result)


if __name__ == "__main__":
    init_state()
    main()

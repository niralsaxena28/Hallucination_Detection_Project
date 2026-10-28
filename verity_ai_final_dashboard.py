"""Verity AI — premium Streamlit research dashboard.
Run from the project root: streamlit run app.py
Uses the real analyze_response() pipeline; it does not simulate verdicts.
"""
import html
import pandas as pd
import streamlit as st

from config import STATUS_HALLUCINATED, STATUS_SUPPORTED, STATUS_UNVERIFIED
from main import analyze_response

st.set_page_config(
    page_title="Verity AI | Research Workbench",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
        st.session_state.analysis_error = "Enter a response before running the analysis."
        st.session_state.analysis_result = None
        return
    try:
        st.session_state.analysis_error = ""
        with st.spinner("Extracting claims, retrieving evidence and running NLI verification…"):
            result = analyze_response(text)
        st.session_state.analysis_result = result
        st.session_state.analysis_input = text
    except Exception as exc:
        st.session_state.analysis_result = None
        st.session_state.analysis_error = (
            "Analysis failed. Check the VS Code terminal for the full error details."
        )
        print(f"Analysis error: {type(exc).__name__}: {exc}")


def inject_css(theme):
    dark = theme == "Dark"
    c = {
        "bg": "#0A1020" if dark else "#F4F7FC",
        "panel": "#111B2E" if dark else "#FFFFFF",
        "panel2": "#151F34" if dark else "#F8FAFE",
        "text": "#E9EEF9" if dark else "#182238",
        "muted": "#9AAAC4" if dark else "#63718A",
        "border": "#293750" if dark else "#DDE5F0",
        "accent": "#8D9BFF" if dark else "#5146E5",
        "accent_soft": "#242E50" if dark else "#ECEBFF",
        "input": "#0E1729" if dark else "#FFFFFF",
    }
    st.markdown(f"""
    <style>
    :root {{ color-scheme: {"dark" if dark else "light"}; }}
    .stApp {{ background: {c['bg']}; color: {c['text']}; }}
    [data-testid="stHeader"] {{ background: transparent; }}
    /* Wider, more spacious sidebar */
    section[data-testid="stSidebar"] {{
        width: 350px !important;
        min-width: 350px !important;
        background: {c['panel']};
        border-right: 1px solid {c['border']};
    }}
    section[data-testid="stSidebar"] > div {{ width: 350px !important; }}
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        padding: 1.2rem 1.15rem 2rem;
    }}
    [data-testid="stSidebar"] * {{ color: {c['text']}; }}
    [data-testid="stSidebar"] hr {{ margin: 1.2rem 0; opacity: .7; }}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        font-size: .88rem; line-height: 1.6;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] {{ gap: .35rem; }}
    [data-testid="stSidebar"] [role="radiogroup"] label {{
        border-radius: 10px; padding: .25rem .35rem;
    }}
    .block-container {{
        max-width: 1560px;
        padding: 1.7rem clamp(1.2rem, 3vw, 3rem) 3.5rem;
    }}
    h1,h2,h3,h4,p,label,.stMarkdown {{ color: {c['text']}; }}
    .brand-mark {{
        display: inline-flex; width: 2.7rem; height: 2.7rem;
        align-items: center; justify-content: center;
        border-radius: 13px; margin-bottom: .75rem;
        background: {c['accent']}; color: #FFFFFF !important;
        font-size: 1.15rem; font-weight: 900;
        box-shadow: 0 8px 22px {c['accent']}33;
    }}
    .eyebrow {{
        color: {c['accent']} !important; font-size: .74rem;
        font-weight: 850; letter-spacing: .15em; text-transform: uppercase;
    }}
    .hero-title {{
        color: {c['text']} !important;
        font-size: clamp(2rem, 3vw, 2.8rem);
        line-height: 1.12; font-weight: 850;
        letter-spacing: -.045em; margin: .45rem 0 .65rem;
        overflow-wrap: anywhere;
    }}
    .subtitle {{
        color: {c['muted']} !important;
        font-size: 1rem; line-height: 1.7;
        margin: 0 0 1.5rem; max-width: 880px;
    }}
    .surface {{
        background: {c['panel']}; border: 1px solid {c['border']};
        border-radius: 16px; padding: 1.1rem 1.2rem;
        box-shadow: {"0 8px 26px #00000012" if not dark else "0 8px 26px #00000018"};
        min-width: 0; box-sizing: border-box;
    }}
    .metric-label {{
        color: {c['muted']} !important; font-size: .82rem;
        font-weight: 700; margin-bottom: .5rem;
    }}
    .metric-value {{
        color: {c['text']} !important; font-size: 1.85rem;
        font-weight: 850; line-height: 1.1; overflow-wrap: anywhere;
    }}
    .metric-foot {{
        color: {c['muted']} !important; font-size: .78rem;
        line-height: 1.5; margin-top: .5rem;
    }}
    .sidebar-tagline {{
        color: {c['muted']} !important; font-size: .88rem; line-height: 1.7;
    }}
    div[data-testid="stTextArea"] textarea {{
        background: {c['input']}; color: {c['text']};
        border: 1px solid {c['border']}; border-radius: 12px;
        line-height: 1.65;
    }}
    div[data-testid="stExpander"] {{
        background: {c['panel']}; border: 1px solid {c['border']};
        border-radius: 12px; overflow-wrap: anywhere;
    }}
    div[data-testid="stMetric"] {{
        background: {c['panel']}; border: 1px solid {c['border']};
        padding: .8rem; border-radius: 12px; min-width: 0;
    }}
    .stButton > button, .stDownloadButton > button {{
        border-radius: 10px; min-height: 2.65rem;
        font-weight: 700; border: 1px solid {c['border']};
        transition: transform .15s ease, border-color .15s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        border-color: {c['accent']}; transform: translateY(-1px);
    }}
    .stButton > button[kind="primary"] {{
        background: {c['accent']}; border-color: {c['accent']}; color: white;
    }}
    hr {{ border-color: {c['border']}; }}
    [data-testid="stDataFrame"] {{ border: 1px solid {c['border']}; border-radius: 12px; }}
    @media (max-width: 900px) {{
        section[data-testid="stSidebar"] {{ width: 290px !important; min-width: 290px !important; }}
        section[data-testid="stSidebar"] > div {{ width: 290px !important; }}
        .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
    }}
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
        st.markdown('<div class="brand-mark">V</div><div class="eyebrow">VERITY AI · LAB</div>',
                    unsafe_allow_html=True)
        st.markdown("## Research Workbench")
        st.markdown(
            '<div class="sidebar-tagline">Claim-level fact checking, evidence tracing, '
            'and transparent AI verification.</div>',
            unsafe_allow_html=True,
        )
        st.divider()
        st.markdown("**WORKSPACE**")
        st.radio(
            "Workspace navigation",
            ["Overview", "Claim analysis", "Evidence & sources", "Pipeline"],
            key="active_view",
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown("**APPEARANCE**")
        st.radio("Theme", ["Dark", "Light"], key="theme_mode", horizontal=True)
        st.divider()
        st.markdown("**VERIFICATION STACK**")
        st.caption("Claim extraction · spaCy NER · Sentence Transformers · FAISS · NLI")
        st.caption("The dashboard displays results from the existing Python pipeline.")
        st.markdown(
            f'<div class="surface" style="padding:.8rem;margin-top:.8rem;">'
            f'<div class="metric-label">Research integrity</div>'
            f'<div style="font-size:.84rem;line-height:1.6;">Unverified means evidence is insufficient or inconclusive. Missing evidence is not proof of falsity.</div></div>',
            unsafe_allow_html=True,
        )


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

    # Two-by-two layout keeps cards readable on typical laptop screens.
    row1 = st.columns(2, gap="medium")
    row2 = st.columns(2, gap="medium")
    items = [
        ("Claims analysed", total, "Factual claims extracted"),
        ("Supported", supported, "Evidence supports claim"),
        ("Contradicted", contradicted, "Pipeline classified as contradicted"),
        ("Unverified", unverified, "Evidence inconclusive or unavailable"),
    ]
    for col, item in zip(row1 + row2, items):
        with col:
            metric_card(*item)

    st.write("")
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        st.markdown("### Verification distribution")
        if total:
            chart = pd.DataFrame({
                "Status": ["Supported", "Contradicted", "Unverified"],
                "Claims": [supported, contradicted, unverified],
            })
            st.bar_chart(chart.set_index("Status"), height=280, horizontal=True)
        else:
            st.info("No factual claims were returned by the extractor.")
    with right:
        st.markdown("### Confidence overview")
        metric_card(
            "Average model confidence",
            fmt_pct(summary.get("average_confidence")),
            "A model-derived estimate; not proof of truth.",
        )


def render_claims(claims):
    if not claims:
        st.info("No factual claims were detected in this response.")
        return
    for claim in claims:
        cid = claim.get("claim_id", "?")
        text = claim.get("text", "(claim text unavailable)")
        status = claim.get("status", STATUS_UNVERIFIED)
        with st.expander(f"{status_icon(status)} [{cid}] {text} · {status}"):
            st.markdown("**Claim**")
            st.write(text)
            a, b, c = st.columns(3)
            a.metric("Status", status)
            b.metric("Semantic similarity", fmt_num(claim.get("similarity")))
            c.metric("Model confidence", fmt_pct(claim.get("confidence")))
            st.markdown(
                f"**NLI result:** {claim.get('nli_label') or 'N/A'} · "
                f"confidence {fmt_num(claim.get('nli_confidence'))}"
            )
            if claim.get("reason"):
                st.markdown("**Explanation**")
                st.write(claim["reason"])

            st.markdown("**Detected entities (spaCy NER)**")
            entities = claim.get("entities") or []
            if entities:
                st.dataframe(
                    pd.DataFrame([
                        {"Entity": entity.get("text", ""), "Label": entity.get("label", "")}
                        for entity in entities
                    ]),
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
                    "No relevant evidence was returned. Missing evidence alone does not prove a claim false."
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
                "Evidence": claim.get("evidence_text", ""),
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
            f'<div class="surface" style="margin-bottom:.7rem;display:flex;gap:1rem;align-items:flex-start;">'
            f'<div style="font-weight:850;color:#8D9BFF;min-width:2rem;">{number}</div>'
            f'<div><b>{html.escape(title)}</b><br><span style="opacity:.75;">{html.escape(description)}</span></div></div>',
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
            '<div class="surface" style="margin-top:1rem;">'
            '<div class="eyebrow">READY FOR ANALYSIS</div>'
            '<h3 style="margin:.5rem 0;">Your research workspace is ready</h3>'
            '<p style="margin-bottom:0;line-height:1.7;">Run an analysis to view claim-level verdicts, retrieved evidence, '
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
            f'<div class="surface" style="white-space:pre-wrap;overflow-wrap:anywhere;'
            f'word-break:normal;max-width:100%;box-sizing:border-box;line-height:1.8;">'
            f'{html.escape(str(corrected))}</div>',
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

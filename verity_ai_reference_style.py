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
        "active_view": "Claim analysis",
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
        "bg": "#0B1517" if dark else "#F6F7F5",
        "sidebar": "#142B32",
        "sidebar_muted": "#A9BFBB",
        "panel": "#122225" if dark else "#FFFFFF",
        "panel2": "#182D2F" if dark else "#FBFCFA",
        "text": "#EAF2EE" if dark else "#1D302F",
        "muted": "#A0B8B1" if dark else "#687B79",
        "border": "#294244" if dark else "#DCE5DF",
        "accent": "#58C4A5" if dark else "#138A72",
        "accent_soft": "#1B3D39" if dark else "#E2F2EC",
        "input": "#0F1D1F" if dark else "#FFFFFF",
        "sidebar": "#142B32",
        "sidebar_text": "#E8F0EE",
        "sidebar_muted": "#A9BFBB",
        "sidebar_border": "#2B454A",
    }
    st.markdown(f"""
    <style>
    :root {{ color-scheme: {"dark" if dark else "light"}; }}
    .stApp {{ background: {c['bg']}; color: {c['text']}; }}
    [data-testid="stHeader"] {{ background: transparent; }}
    /* Wider, more spacious sidebar */
    section[data-testid="stSidebar"] {{
        width: 300px !important; min-width: 300px !important;
        background: {c['sidebar']} !important;
        border-right: 1px solid {c['sidebar_border']};
    }}
    section[data-testid="stSidebar"] > div {{ width: 300px !important; }}
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        padding: 1rem .95rem 1.5rem; background: {c['sidebar']} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        color: #E8F0EE !important;
    }}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
        color: {c['sidebar_muted']} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        color: {c['sidebar_text']} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
        color: {c['sidebar_muted']} !important;
    }}
    [data-testid="stSidebar"] hr {{
        margin: 1rem 0; border-color: {c['sidebar_border']}; opacity: 1;
    }}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        font-size: .84rem; line-height: 1.55;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] {{ gap: .35rem; }}
    [data-testid="stSidebar"] [role="radiogroup"] label {{
        border-radius: 10px; padding: .25rem .35rem;
    }}
    .block-container {{
        width: 100% !important; max-width: 1260px !important;
        min-width: 0 !important;
        padding: 1.35rem clamp(.9rem, 2vw, 1.8rem) 2.8rem;
        box-sizing: border-box;
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
        font-size: clamp(2rem, 2.65vw, 2.55rem);
        line-height: 1.13; font-weight: 800;
        letter-spacing: -.045em; margin: .5rem 0 .65rem;
        overflow-wrap: anywhere;
    }}
    .subtitle {{
        color: {c['muted']} !important;
        font-size: 1rem; line-height: 1.7;
        margin: 0 0 1.5rem; max-width: 880px;
    }}
    .surface {{
        background: {c['panel']}; border: 1px solid {c['border']};
        border-radius: 16px; padding: 1.15rem 1.25rem;
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
        color: {c['sidebar_muted']} !important; font-size: .84rem; line-height: 1.6;
    }}
    .sidebar-section-label {{
        color: #9FB8B5 !important; font-size: .74rem;
        font-weight: 800; letter-spacing: .06em; margin: .2rem 0 .65rem;
    }}
    .sidebar-status {{
        display:flex; align-items:center; gap:.5rem; color:#D7E7E3;
        font-size:.82rem; padding:.35rem 0;
    }}
    .status-dot {{
        display:inline-block; width:.55rem; height:.55rem; border-radius:50%;
        background:#58C4A5; box-shadow:0 0 0 3px #58C4A522;
    }}
    .page-kicker {{
        color: {c['accent']} !important; font-size: .73rem;
        font-weight: 800; letter-spacing: .1em; margin-bottom: .45rem;
    }}
    .page-title {{
        color: {c['text']} !important; font-size: 1.7rem;
        font-weight: 780; letter-spacing: -.035em; line-height: 1.2;
        margin-bottom: .45rem;
    }}
    .page-subtitle {{
        color: {c['muted']} !important; font-size: .9rem;
        line-height: 1.6; margin-bottom: 1.15rem;
    }}
    .input-meta {{
        color: {c['muted']} !important; font-size: .72rem;
        margin: -.2rem 0 .65rem; text-align: right;
    }}
    [data-testid="stSidebar"] .stButton > button {{
        text-align: left !important; justify-content: flex-start !important;
        min-height: 2.45rem; padding: .45rem .65rem !important;
        border-color: transparent !important; box-shadow: none !important;
        background: transparent !important; color: #D5E3E0 !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: #24534F !important; color: #FFFFFF !important;
        border-color: #24534F !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: #1B3D40 !important; border-color: #1B3D40 !important;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] label {{ color: #DCE8E5 !important; }}
    div[data-testid="stTextArea"] textarea {{
        width: 100% !important; min-height: 148px !important; max-height: 220px;
        width: 100% !important; min-height: 105px !important;
        background: {c['input']} !important; color: {c['text']} !important;
        -webkit-text-fill-color: {c['text']} !important;
        border: 1px solid {c['border']} !important; border-radius: 11px !important;
        line-height: 1.65; padding: .8rem .9rem; box-sizing: border-box;
    }}
    div[data-testid="stTextArea"] textarea::placeholder {{
        color: {c['muted']} !important;
        -webkit-text-fill-color: {c['muted']} !important; opacity: 1 !important;
    }}
    div[data-testid="stTextArea"] textarea::placeholder {{
        color: {c['muted']} !important; -webkit-text-fill-color: {c['muted']} !important; opacity: 1 !important;
    }}
    div[data-testid="stExpander"] {{
        background: {c['panel']}; border: 1px solid {c['border']};
        border-radius: 12px; overflow-wrap: anywhere;
    }}
    div[data-testid="stMetric"] {{
        background: {c['panel']}; border: 1px solid {c['border']};
        padding: .8rem; border-radius: 12px; min-width: 0;
    }}
    /* Explicit button colours: Streamlit theme defaults must not reduce contrast. */
    .stButton > button, .stDownloadButton > button {{
        width: 100%; border-radius: 10px !important; min-height: 2.65rem;
        padding: .5rem .8rem; font-weight: 650 !important;
        border: 1px solid {c['border']} !important;
        background: {c['panel']} !important; color: {c['text']} !important;
        box-shadow: 0 1px 3px rgba(12,35,31,.05);
        transition: border-color .15s ease, box-shadow .15s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        border-color: {c['accent']} !important;
        box-shadow: 0 3px 12px rgba(19,138,114,.12);
    }}
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"]:hover {{
        background: {c['accent']} !important; border-color: {c['accent']} !important;
        color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 750 !important;
    }}
    .stButton > button:focus, .stDownloadButton > button:focus {{
        outline: 2px solid {c['accent']} !important;
        outline-offset: 2px;
    }}
    [data-testid="stTextArea"] textarea:focus {{
        border-color: {c['accent']} !important;
        box-shadow: 0 0 0 1px {c['accent']} !important;
    }}
    [data-testid="stAppViewBlockContainer"], [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"],
    [data-testid="column"], [data-testid="stElementContainer"] {{
        min-width: 0 !important; box-sizing: border-box;
    }}
    [data-testid="stMain"] {{ min-width: 0 !important; overflow-x: hidden; }}
    .stApp, button, textarea, input, [data-testid="stMarkdownContainer"] {{
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 18px;
    }}
    [data-testid="stCaptionContainer"] p {{
        color: {c['muted']} !important;
        line-height: 1.65;
    }}
    .stApp, button, textarea, input, [data-testid="stMarkdownContainer"] {{
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    hr {{ border-color: {c['border']}; }}
    [data-testid="stDataFrame"] {{ border: 1px solid {c['border']}; border-radius: 12px; }}
    [data-testid="stBarChart"] {{ background: {c['panel']}; border: 1px solid {c['border']}; border-radius: 14px; padding: .6rem; }}
    [data-testid="stPlotlyChart"] > div {{ border: 1px solid {c['border']}; border-radius: 14px; }}
    h2, h3 {{ letter-spacing: -.025em; }}
    [data-testid="stExpander"] summary {{ font-weight: 650; }}
    [data-testid="stPlotlyChart"] {{ border-radius: 14px; overflow: hidden; }}
    .section-kicker {{ color: {c['accent']} !important; font-size: .74rem; letter-spacing: .13em; font-weight: 800; text-transform: uppercase; }}
    @media (max-width: 900px) {{
        section[data-testid="stSidebar"] {{ width: 270px !important; min-width: 270px !important; }}
        section[data-testid="stSidebar"] > div {{ width: 270px !important; }}
        .block-container {{ padding-left: .8rem; padding-right: .8rem; }}
        .hero-title {{ font-size: clamp(1.8rem, 5vw, 2.3rem); }}
    }}
    @media (max-width: 600px) {{
        .block-container {{ padding: 1rem .7rem 2rem; }}
        .surface {{ padding: .85rem; }}
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
        st.markdown('<div class="sidebar-section-label">WORKSPACE</div>', unsafe_allow_html=True)
        nav_items = [
            ("▦", "Overview"),
            ("◎", "Claim analysis"),
            ("◇", "Evidence & sources"),
            ("⌘", "Pipeline"),
        ]
        for glyph, label in nav_items:
            active = st.session_state.active_view == label
            if st.button(
                f"{glyph}    {label}",
                key=f"nav_{label}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                st.session_state.active_view = label
                st.rerun()
        st.divider()
        st.markdown('<div class="sidebar-section-label">APPEARANCE</div>', unsafe_allow_html=True)
        st.radio("Theme", ["Dark", "Light"], key="theme_mode", horizontal=True)
        st.divider()
        st.markdown('<div class="sidebar-section-label">SYSTEM STATUS</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-status"><span class="status-dot"></span> Python verification pipeline</div>',
            unsafe_allow_html=True,
        )
        st.caption("Claim extraction · spaCy NER · Sentence Transformers · FAISS · NLI")
        st.caption("Verdicts and evidence are returned by the existing Python pipeline.")


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
            try:
                import plotly.express as px
                fig = px.bar(
                    chart, x="Claims", y="Status", orientation="h",
                    text="Claims", color="Status",
                    color_discrete_map={
                        "Supported": "#58C4A5" if st.session_state.theme_mode == "Dark" else "#137C68",
                        "Contradicted": "#E87979",
                        "Unverified": "#D6A84F",
                    },
                )
                fig.update_layout(
                    height=290, margin=dict(l=8, r=12, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#EAF2EE" if st.session_state.theme_mode == "Dark" else "#1D302F"),
                    showlegend=False,
                    xaxis=dict(title="", showgrid=True, gridcolor="#294244" if st.session_state.theme_mode == "Dark" else "#E4EAE5", rangemode="tozero"),
                    yaxis=dict(title="", categoryorder="array", categoryarray=["Unverified", "Contradicted", "Supported"]),
                )
                fig.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            except ImportError:
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

    page_titles = {
        "Overview": ("Overview", "Review the latest claim-verification results."),
        "Claim analysis": ("Claim analysis", "Inspect claims and trace their supporting evidence."),
        "Evidence & sources": ("Evidence & sources", "Review the passages and source links returned by retrieval."),
        "Pipeline": ("Verification pipeline", "Understand the processing stages used by the current system."),
    }
    page_title, page_subtitle = page_titles.get(
        st.session_state.active_view,
        ("Claim analysis", "Inspect claims and trace their supporting evidence.")
    )
    st.markdown(
        f'<div class="page-kicker">RESEARCH / VERIFICATION</div>'
        f'<div class="page-title">{html.escape(page_title)}</div>'
        f'<div class="page-subtitle">{html.escape(page_subtitle)}</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("#### Analyse an AI response")
        st.caption("Submit a generated response to identify factual claims and assess the available evidence.")
        st.text_area(
            "Response text",
            key="response_input",
            height=105,
            placeholder="Paste an LLM-generated response to begin verification…",
            label_visibility="collapsed",
        )
        word_count = len(st.session_state.response_input.split())
        st.markdown(
            f'<div class="input-meta">{word_count} words · Your text is processed by the local verification pipeline</div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns([1.05, .9, 1.0])
        with c1:
            st.button("Run analysis →", type="primary", use_container_width=True, on_click=run_analysis)
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
    st.markdown('<div class="section-kicker">REPORT / LIVE PIPELINE OUTPUT</div>', unsafe_allow_html=True)
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

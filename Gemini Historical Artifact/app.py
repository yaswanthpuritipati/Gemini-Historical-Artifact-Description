<<<<<<< HEAD:app.py
import streamlit as st
import google.generativeai as genai
from PIL import Image
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gemini Historical Artifact Explorer",
    page_icon="🏛️",
    layout="wide",
)

# ─── Custom CSS — Premium Museum Theme ─────────────────────────────────────────
st.markdown("""
<style>
/* ── Imports ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root variables — Warm Terracotta & Cream ────────────────── */
:root {
    --terra: #C4693D;
    --terra-light: #E8A878;
    --terra-dark: #9B4A28;
    --terra-deeper: #7A3A1E;
    --cream: #F5ECD7;
    --cream-dark: #D9CDB5;
    --parchment: #EDE3CC;
    --bg-primary: #1A1512;
    --bg-secondary: #201914;
    --bg-card: rgba(38, 30, 24, 0.8);
    --bg-card-solid: #282018;
    --bg-card-hover: rgba(45, 36, 28, 0.9);
    --text-primary: #F0E8D8;
    --text-secondary: #D4C8B4;
    --text-muted: #A89880;
    --border-terra: rgba(196, 105, 61, 0.25);
    --border-terra-hover: rgba(196, 105, 61, 0.5);
    --glow-terra: rgba(196, 105, 61, 0.12);
    --glow-terra-strong: rgba(196, 105, 61, 0.25);
    --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.3);
    --shadow-medium: 0 8px 32px rgba(0, 0, 0, 0.4);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Global overrides ────────────────────────────────────────── */
.stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1000px;
}

/* subtle parchment texture overlay */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(196, 105, 61, 0.03) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(196, 105, 61, 0.02) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(232, 168, 120, 0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Animations ─────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes shimmer {
    0%   { filter: brightness(1); }
    100% { filter: brightness(1.15); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.9); }
}
@keyframes floatIcon {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

/* ── Hero header ─────────────────────────────────────────────── */
.hero-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    position: relative;
    animation: fadeInUp 0.8s ease-out;
}
.hero-icon {
    font-size: 3rem;
    display: inline-block;
    animation: floatIcon 3s ease-in-out infinite;
    margin-bottom: 0.5rem;
}
.hero-header h1 {
    font-family: 'Cinzel', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--terra-light);
    text-shadow: 0 0 30px rgba(196, 105, 61, 0.3), 0 2px 4px rgba(0, 0, 0, 0.3);
    margin-bottom: 0.4rem;
    line-height: 1.2;
    letter-spacing: 1px;
    animation: shimmer 3s ease-in-out infinite alternate;
}
.hero-header .subtitle {
    font-family: 'Cormorant Garamond', serif;
    color: var(--text-muted);
    font-size: 1.1rem;
    font-weight: 400;
    font-style: italic;
    letter-spacing: 0.3px;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.5;
}

/* ── Ornamental divider ──────────────────────────────────────── */
.ornament-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 1.2rem 0;
    opacity: 0.6;
}
.ornament-divider .line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--terra), transparent);
}
.ornament-divider .diamond {
    width: 6px;
    height: 6px;
    background: var(--terra);
    transform: rotate(45deg);
    flex-shrink: 0;
}

/* ── Section label ───────────────────────────────────────────── */
.section-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--terra);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border-terra);
}

/* ── Glass card (refined) ────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-terra);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
    transition: all var(--transition);
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 10%, var(--terra) 50%, transparent 90%);
    opacity: 0.5;
}
.glass-card:hover {
    border-color: var(--border-terra-hover);
    box-shadow: var(--shadow-soft), 0 0 30px var(--glow-terra);
    transform: translateY(-1px);
}
.glass-card h3 {
    font-family: 'Cinzel', serif;
    color: var(--terra-light);
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Tabs styling ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--bg-card-solid);
    border-radius: var(--radius-md);
    padding: 5px;
    border: 1px solid var(--border-terra);
    box-shadow: var(--shadow-soft);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    color: var(--text-muted);
    border-radius: var(--radius-sm);
    padding: 0.65rem 1.5rem;
    transition: all var(--transition);
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary);
    background: rgba(196, 105, 61, 0.08);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--terra-dark), var(--terra)) !important;
    color: var(--cream) !important;
    font-weight: 600;
    box-shadow: 0 2px 12px rgba(196, 105, 61, 0.3);
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.2rem !important;
}

/* ── Buttons ─────────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    background: linear-gradient(135deg, var(--terra-dark), var(--terra));
    color: var(--cream);
    border: none;
    border-radius: var(--radius-md);
    padding: 0.8rem 2rem;
    transition: all var(--transition);
    box-shadow: 0 4px 15px rgba(196, 105, 61, 0.25);
    letter-spacing: 0.3px;
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, transparent, rgba(255,255,255,0.1), transparent);
    opacity: 0;
    transition: opacity var(--transition);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(196, 105, 61, 0.4);
}
.stButton > button:hover::before {
    opacity: 1;
}
.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(196, 105, 61, 0.3);
}

/* ── Download button ─────────────────────────────────────────── */
.stDownloadButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    background: transparent;
    color: var(--terra-light);
    border: 1px solid var(--border-terra);
    border-radius: var(--radius-md);
    padding: 0.6rem 1.5rem;
    transition: all var(--transition);
}
.stDownloadButton > button:hover {
    background: var(--glow-terra);
    border-color: var(--terra);
    box-shadow: 0 0 20px var(--glow-terra);
    transform: translateY(-1px);
}

/* ── Inputs ──────────────────────────────────────────────────── */
.stTextInput > div > div > input {
    background: var(--bg-card-solid) !important;
    border: 1px solid var(--border-terra) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: all var(--transition) !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--text-muted) !important;
    font-style: italic !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--terra) !important;
    box-shadow: 0 0 0 3px var(--glow-terra), 0 0 15px var(--glow-terra) !important;
}

/* ── Slider ──────────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--terra) !important;
    border: 2px solid var(--terra-light) !important;
    width: 18px !important;
    height: 18px !important;
}
.stSlider [data-testid="stTickBar"] {
    background: linear-gradient(90deg, var(--terra-dark), var(--terra)) !important;
}
.stSlider p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    color: var(--text-secondary) !important;
}

/* ── File uploader ───────────────────────────────────────────── */
.stFileUploader > div {
    border: 2px dashed var(--border-terra) !important;
    border-radius: var(--radius-lg) !important;
    background: var(--bg-card-solid) !important;
    transition: all var(--transition) !important;
    padding: 1.5rem !important;
}
.stFileUploader > div:hover {
    border-color: var(--terra) !important;
    background: var(--bg-card-hover) !important;
    box-shadow: 0 0 20px var(--glow-terra) !important;
}

/* ── Result card ─────────────────────────────────────────────── */
.result-card {
    background: linear-gradient(145deg, rgba(38,30,24,0.9), rgba(32,25,20,0.95));
    backdrop-filter: blur(24px);
    border: 1px solid var(--border-terra);
    border-radius: var(--radius-xl);
    padding: 1.8rem 2rem;
    margin: 1.2rem 0;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s ease-out;
    box-shadow: var(--shadow-medium);
}
.result-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--terra-dark), var(--terra), var(--terra-light), var(--terra), var(--terra-dark));
}
.result-card::after {
    content: "";
    position: absolute;
    top: 3px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 2px;
    background: var(--terra-light);
    border-radius: 2px;
    opacity: 0.5;
}
.result-card h3 {
    font-family: 'Cinzel', serif;
    color: var(--terra-light);
    margin-bottom: 0.8rem;
    font-size: 1.1rem;
    padding-top: 0.3rem;
}

/* ── Word-count badge ────────────────────────────────────────── */
.word-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: linear-gradient(135deg, var(--terra-dark), var(--terra));
    color: var(--cream);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.7rem;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Sidebar ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E1812 0%, var(--bg-primary) 100%);
    border-right: 1px solid var(--border-terra);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 0.5rem;
}

.sidebar-brand {
    text-align: center;
    padding: 1.5rem 1rem 0.8rem;
}
.sidebar-brand .brand-icon {
    font-size: 2.2rem;
    display: inline-block;
    animation: floatIcon 3s ease-in-out infinite;
    margin-bottom: 0.3rem;
}
.sidebar-brand h2 {
    font-family: 'Cinzel', serif;
    font-size: 1.15rem;
    font-weight: 600;
    background: linear-gradient(135deg, var(--cream), var(--terra-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
    letter-spacing: 0.5px;
}
.sidebar-brand .version {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    color: var(--text-muted);
    background: rgba(196,105,61,0.08);
    padding: 3px 12px;
    border-radius: 20px;
    border: 1px solid rgba(196,105,61,0.15);
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* status indicator */
.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.6rem 0.8rem;
    border-radius: var(--radius-sm);
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.5rem 0;
    transition: all var(--transition);
}
.status-indicator.active {
    background: rgba(107, 142, 90, 0.1);
    border: 1px solid rgba(107, 142, 90, 0.2);
    color: #8FB87A;
}
.status-indicator.error {
    background: rgba(196, 93, 74, 0.1);
    border: 1px solid rgba(196, 93, 74, 0.2);
    color: #D4806E;
}
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
}
.status-dot.active  { background: #6B8E5A; box-shadow: 0 0 6px #6B8E5A; }
.status-dot.error   { background: #C45D4A; box-shadow: 0 0 6px #C45D4A; }

/* fact card */
.fact-card {
    background: rgba(196,105,61,0.05);
    border: 1px solid rgba(196,105,61,0.12);
    border-left: 3px solid var(--terra);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 0.9rem 1rem;
    margin: 0.6rem 0;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.6;
    font-style: italic;
}

/* sidebar info list */
.sidebar-info {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: var(--text-muted);
    padding: 0.5rem 0;
}
.sidebar-info .info-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(196,105,61,0.06);
}
.sidebar-info .info-item:last-child {
    border-bottom: none;
}
.sidebar-info .info-icon {
    font-size: 0.85rem;
    width: 20px;
    text-align: center;
}

/* ── Streamlit element tweaks ────────────────────────────────── */
.stAlert > div { border-radius: var(--radius-md) !important; }
.stSpinner > div { border-color: var(--terra) !important; }
.stImage {
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-soft);
    border: 1px solid var(--border-terra);
}
h1, h2, h3, h4 { font-family: 'Inter', sans-serif; }
.stMarkdown {
    font-family: 'Inter', sans-serif;
    line-height: 1.7;
}
.stMarkdown a { color: var(--terra-light) !important; text-decoration: underline !important; text-underline-offset: 3px; }
.stMarkdown a:hover { color: var(--terra) !important; }

/* expander styling */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: 1px solid var(--border-terra) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Footer ──────────────────────────────────────────────────── */
.app-footer {
    text-align: center;
    padding: 1.5rem 0 1rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}
.app-footer span { color: var(--terra-light); font-weight: 500; }
.app-footer .footer-links {
    margin-top: 0.4rem;
    font-size: 0.7rem;
    opacity: 0.6;
}

/* ── Helper text styling ─────────────────────────────────────── */
.helper-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Image preview container ─────────────────────────────────── */
.img-preview-container {
    display: flex;
    justify-content: center;
    padding: 1rem 0;
    animation: fadeIn 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ─── API Configuration ────────────────────────────────────────────────────────
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# Try to get API key from environment or streamlit secrets
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Fallback to Streamlit secrets if available
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        pass

try:
    if api_key:
        genai.configure(api_key=api_key)
        st.session_state.api_key_configured = True
    else:
        st.session_state.api_key_configured = False
except Exception as e:
    st.session_state.api_key_configured = False

# ─── Historical facts ─────────────────────────────────────────────────────────
HISTORICAL_FACTS = [
    "The Great Pyramid of Giza was the tallest man-made structure for 3,800 years.",
    "Leonardo da Vinci wrote most of his notes in mirror script — backward writing.",
    "The Rosetta Stone was the key to deciphering Egyptian hieroglyphics.",
    "The Bayeux Tapestry is 70 meters long and depicts the Norman conquest of 1066.",
    "Tutankhamun's tomb contained over 5,000 artifacts when discovered in 1922.",
    "The Colosseum in Rome could hold up to 50,000 spectators in ancient times.",
    "The Library of Alexandria held hundreds of thousands of scrolls from the ancient world.",
    "The Antikythera mechanism is the world's oldest known analog computer.",
    "Medieval knights' armor weighed up to 50 lbs but was evenly distributed.",
    "The Dead Sea Scrolls are among the oldest biblical manuscripts — 2,000 years old.",
]

# ─── Helper ────────────────────────────────────────────────────────────────────
def get_gemini_response(prompt, image=None):
    """Generate response from Gemini model."""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        if image:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">🏛️</div>
        <h2>Artifact Explorer</h2>
        <span class="version">v2.0 · Gemini AI</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    # API Status
    if st.session_state.api_key_configured:
        st.markdown(
            '<div class="status-indicator active">'
            '<span class="status-dot active"></span>'
            'Gemini API Connected</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-indicator error">'
            '<span class="status-dot error"></span>'
            'API Disconnected</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    # Random fact
    st.markdown('<div class="section-label">💡 Did You Know?</div>', unsafe_allow_html=True)
    fact = random.choice(HISTORICAL_FACTS)
    st.markdown(f'<div class="fact-card">{fact}</div>', unsafe_allow_html=True)

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    # Capabilities
    st.markdown('<div class="section-label">🔧 Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info">
        <div class="info-item"><span class="info-icon">📝</span> Text-based artifact descriptions</div>
        <div class="info-item"><span class="info-icon">🖼️</span> Image-based artifact analysis</div>
        <div class="info-item"><span class="info-icon">📥</span> Downloadable research reports</div>
        <div class="info-item"><span class="info-icon">🎯</span> Adjustable detail level</div>
        <div class="info-item"><span class="info-icon">🤖</span> Powered by Gemini 2.5 Flash</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    with st.expander("ℹ️ About"):
        st.markdown("""
        Upload an image of any historical artifact or enter its name,
        and **Gemini 2.5 Flash** will generate a rich, detailed description
        covering its origin, significance, and modern context.
        
        Built for historians, museum curators, and history enthusiasts.
        """)

# ─── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-icon">🏛️</div>
    <h1>Historical Artifact Explorer</h1>
    <p class="subtitle">Uncover the stories behind humanity's greatest treasures — powered by Gemini AI</p>
</div>
<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>
""", unsafe_allow_html=True)

# ─── Main Tabs ────────────────────────────────────────────────────────────────
tab_text, tab_image = st.tabs(["✍️  Describe by Name", "🖼️  Analyze from Image"])

# ── Tab 1 — Text description ─────────────────────────────────────────────────
with tab_text:
    st.markdown("""
    <div class="glass-card">
        <h3>📝 Enter Artifact Details</h3>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-muted); margin: 0;">
            Type the name of any artifact, monument, or historical period to generate a detailed scholarly description.
        </p>
    </div>
    """, unsafe_allow_html=True)

    artifact_name = st.text_input(
        "Artifact name or historical period",
        placeholder="e.g., Tutankhamun's Golden Mask, Terracotta Army, Viking Runestone…",
        label_visibility="collapsed",
    )

    col_slider, col_badge = st.columns([4, 1])
    with col_slider:
        word_count = st.slider(
            "Description length (words)",
            min_value=500, max_value=2000, value=1000, step=100,
        )
    with col_badge:
        st.markdown("")  # spacing
        st.markdown(
            f'<div style="padding-top: 1.8rem;"><span class="word-badge">≈ {word_count} words</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")  # spacer

    if st.button("🚀 Generate Description", key="btn_text", use_container_width=True):
        if not st.session_state.api_key_configured:
            st.error("⚠️ API key is not configured. Check the sidebar for status.")
        elif not artifact_name.strip():
            st.warning("Please enter an artifact name or historical period first.")
        else:
            with st.spinner("🔮 Gemini is researching the archives…"):
                prompt = f"""Generate a detailed and engaging description of **{artifact_name}**.

Include the following sections:
1. **Historical Background** — Origin, time period, cultural context
2. **Physical Characteristics** — Materials, dimensions, notable features
3. **Historical Significance** — Importance and lasting impact
4. **Interesting Facts** — Unique or lesser-known details
5. **Modern Context** — Relevance today and current location

Write approximately {word_count} words in an engaging, informative tone suitable for historians, museum curators, and history enthusiasts. Use markdown formatting with headers."""

                response = get_gemini_response(prompt)

            # Result
            st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)
            word_ct = len(response.split())
            st.markdown(
                f'<div class="result-card">'
                f'<h3>📚 {artifact_name}</h3>'
                f'<span class="word-badge">{word_ct} words</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown(response)

            st.markdown("")  # spacer
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.download_button(
                    "📥 Download as Text",
                    data=response,
                    file_name=f"{artifact_name.replace(' ', '_')}_description.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with col_b:
                st.download_button(
                    "📋 Download as Markdown",
                    data=response,
                    file_name=f"{artifact_name.replace(' ', '_')}_description.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

# ── Tab 2 — Image analysis ───────────────────────────────────────────────────
with tab_image:
    st.markdown("""
    <div class="glass-card">
        <h3>🖼️ Upload an Artifact Image</h3>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-muted); margin: 0;">
            Upload a photo of any artifact — pottery, sculpture, manuscript, weapon, jewelry, architecture — for AI-powered analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drag and drop or browse — JPG, PNG, GIF, WEBP",
        type=["jpg", "jpeg", "png", "gif", "webp"],
        label_visibility="collapsed",
    )

    col_slider2, col_badge2 = st.columns([4, 1])
    with col_slider2:
        img_word_count = st.slider(
            "Analysis length (words)",
            min_value=500, max_value=2000, value=1000, step=100,
            key="img_slider",
        )
    with col_badge2:
        st.markdown("")
        st.markdown(
            f'<div style="padding-top: 1.8rem;"><span class="word-badge">≈ {img_word_count} words</span></div>',
            unsafe_allow_html=True,
        )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(image, caption="📷 Uploaded Artifact", width=300)

    st.markdown("")  # spacer

    if st.button("🔍 Analyze Artifact", key="btn_img", use_container_width=True):
        if not st.session_state.api_key_configured:
            st.error("⚠️ API key is not configured. Check the sidebar for status.")
        elif uploaded_file is None:
            st.warning("Please upload an image of the artifact first.")
        else:
            with st.spinner("🔮 Gemini is examining the artifact…"):
                image_parts = {
                    "mime_type": uploaded_file.type,
                    "data": uploaded_file.getvalue(),
                }
                prompt = f"""You are a world-class historian and artifact expert.
Analyze the artifact shown in this image and provide a detailed description.

Include:
1. **Identification** — What is this artifact? Classify its type and likely origin.
2. **Historical Background** — Period, culture, and context.
3. **Physical Analysis** — Materials, craftsmanship, condition.
4. **Significance** — Why is it important?
5. **Interesting Facts** — Unique details.

Write approximately {img_word_count} words in an engaging, scholarly tone. Use markdown formatting with headers."""

                response = get_gemini_response(prompt, image_parts)

            st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)
            word_ct = len(response.split())
            st.markdown(
                f'<div class="result-card">'
                f'<h3>🔎 Artifact Analysis</h3>'
                f'<span class="word-badge">{word_ct} words</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown(response)

            st.markdown("")  # spacer
            col_dl1, col_dl2 = st.columns([1, 1])
            with col_dl1:
                st.download_button(
                    "📥 Download Analysis",
                    data=response,
                    file_name="artifact_analysis.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with col_dl2:
                st.download_button(
                    "📋 Download as Markdown",
                    data=response,
                    file_name="artifact_analysis.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>
<div class="app-footer">
    Powered by <span>Google Gemini 2.5 Flash</span> · Built for Historical Research<br>
    <div class="footer-links">Crafted with care for historians & museum curators</div>
</div>
""", unsafe_allow_html=True)
=======
import streamlit as st
import google.generativeai as genai
from PIL import Image
import random
import time

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gemini Historical Artifact Explorer",
    page_icon="🏛️",
    layout="wide",
)

# ─── Custom CSS — Premium Museum Theme ─────────────────────────────────────────
st.markdown("""
<style>
/* ── Imports ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root variables — Warm Terracotta & Cream ────────────────── */
:root {
    --terra: #C4693D;
    --terra-light: #E8A878;
    --terra-dark: #9B4A28;
    --terra-deeper: #7A3A1E;
    --cream: #F5ECD7;
    --cream-dark: #D9CDB5;
    --parchment: #EDE3CC;
    --bg-primary: #1A1512;
    --bg-secondary: #201914;
    --bg-card: rgba(38, 30, 24, 0.8);
    --bg-card-solid: #282018;
    --bg-card-hover: rgba(45, 36, 28, 0.9);
    --text-primary: #F0E8D8;
    --text-secondary: #D4C8B4;
    --text-muted: #A89880;
    --border-terra: rgba(196, 105, 61, 0.25);
    --border-terra-hover: rgba(196, 105, 61, 0.5);
    --glow-terra: rgba(196, 105, 61, 0.12);
    --glow-terra-strong: rgba(196, 105, 61, 0.25);
    --shadow-soft: 0 4px 20px rgba(0, 0, 0, 0.3);
    --shadow-medium: 0 8px 32px rgba(0, 0, 0, 0.4);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Global overrides ────────────────────────────────────────── */
.stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1000px;
}

/* subtle parchment texture overlay */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(196, 105, 61, 0.03) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(196, 105, 61, 0.02) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(232, 168, 120, 0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Animations ─────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes shimmer {
    0%   { filter: brightness(1); }
    100% { filter: brightness(1.15); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.9); }
}
@keyframes floatIcon {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

/* ── Hero header ─────────────────────────────────────────────── */
.hero-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    position: relative;
    animation: fadeInUp 0.8s ease-out;
}
.hero-icon {
    font-size: 3rem;
    display: inline-block;
    animation: floatIcon 3s ease-in-out infinite;
    margin-bottom: 0.5rem;
}
.hero-header h1 {
    font-family: 'Cinzel', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--terra-light);
    text-shadow: 0 0 30px rgba(196, 105, 61, 0.3), 0 2px 4px rgba(0, 0, 0, 0.3);
    margin-bottom: 0.4rem;
    line-height: 1.2;
    letter-spacing: 1px;
    animation: shimmer 3s ease-in-out infinite alternate;
}
.hero-header .subtitle {
    font-family: 'Cormorant Garamond', serif;
    color: var(--text-muted);
    font-size: 1.1rem;
    font-weight: 400;
    font-style: italic;
    letter-spacing: 0.3px;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.5;
}

/* ── Ornamental divider ──────────────────────────────────────── */
.ornament-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 1.2rem 0;
    opacity: 0.6;
}
.ornament-divider .line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--terra), transparent);
}
.ornament-divider .diamond {
    width: 6px;
    height: 6px;
    background: var(--terra);
    transform: rotate(45deg);
    flex-shrink: 0;
}

/* ── Section label ───────────────────────────────────────────── */
.section-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--terra);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border-terra);
}

/* ── Glass card (refined) ────────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-terra);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
    transition: all var(--transition);
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 10%, var(--terra) 50%, transparent 90%);
    opacity: 0.5;
}
.glass-card:hover {
    border-color: var(--border-terra-hover);
    box-shadow: var(--shadow-soft), 0 0 30px var(--glow-terra);
    transform: translateY(-1px);
}
.glass-card h3 {
    font-family: 'Cinzel', serif;
    color: var(--terra-light);
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Tabs styling ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--bg-card-solid);
    border-radius: var(--radius-md);
    padding: 5px;
    border: 1px solid var(--border-terra);
    box-shadow: var(--shadow-soft);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    color: var(--text-muted);
    border-radius: var(--radius-sm);
    padding: 0.65rem 1.5rem;
    transition: all var(--transition);
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary);
    background: rgba(196, 105, 61, 0.08);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--terra-dark), var(--terra)) !important;
    color: var(--cream) !important;
    font-weight: 600;
    box-shadow: 0 2px 12px rgba(196, 105, 61, 0.3);
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.2rem !important;
}

/* ── Buttons ─────────────────────────────────────────────────── */
.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    background: linear-gradient(135deg, var(--terra-dark), var(--terra));
    color: var(--cream);
    border: none;
    border-radius: var(--radius-md);
    padding: 0.8rem 2rem;
    transition: all var(--transition);
    box-shadow: 0 4px 15px rgba(196, 105, 61, 0.25);
    letter-spacing: 0.3px;
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, transparent, rgba(255,255,255,0.1), transparent);
    opacity: 0;
    transition: opacity var(--transition);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(196, 105, 61, 0.4);
}
.stButton > button:hover::before {
    opacity: 1;
}
.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(196, 105, 61, 0.3);
}

/* ── Download button ─────────────────────────────────────────── */
.stDownloadButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    background: transparent;
    color: var(--terra-light);
    border: 1px solid var(--border-terra);
    border-radius: var(--radius-md);
    padding: 0.6rem 1.5rem;
    transition: all var(--transition);
}
.stDownloadButton > button:hover {
    background: var(--glow-terra);
    border-color: var(--terra);
    box-shadow: 0 0 20px var(--glow-terra);
    transform: translateY(-1px);
}

/* ── Inputs ──────────────────────────────────────────────────── */
.stTextInput > div > div > input {
    background: var(--bg-card-solid) !important;
    border: 1px solid var(--border-terra) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: all var(--transition) !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--text-muted) !important;
    font-style: italic !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--terra) !important;
    box-shadow: 0 0 0 3px var(--glow-terra), 0 0 15px var(--glow-terra) !important;
}

/* ── Slider ──────────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--terra) !important;
    border: 2px solid var(--terra-light) !important;
    width: 18px !important;
    height: 18px !important;
}
.stSlider [data-testid="stTickBar"] {
    background: linear-gradient(90deg, var(--terra-dark), var(--terra)) !important;
}
.stSlider p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    color: var(--text-secondary) !important;
}

/* ── File uploader ───────────────────────────────────────────── */
.stFileUploader > div {
    border: 2px dashed var(--border-terra) !important;
    border-radius: var(--radius-lg) !important;
    background: var(--bg-card-solid) !important;
    transition: all var(--transition) !important;
    padding: 1.5rem !important;
}
.stFileUploader > div:hover {
    border-color: var(--terra) !important;
    background: var(--bg-card-hover) !important;
    box-shadow: 0 0 20px var(--glow-terra) !important;
}

/* ── Result card ─────────────────────────────────────────────── */
.result-card {
    background: linear-gradient(145deg, rgba(38,30,24,0.9), rgba(32,25,20,0.95));
    backdrop-filter: blur(24px);
    border: 1px solid var(--border-terra);
    border-radius: var(--radius-xl);
    padding: 1.8rem 2rem;
    margin: 1.2rem 0;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s ease-out;
    box-shadow: var(--shadow-medium);
}
.result-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--terra-dark), var(--terra), var(--terra-light), var(--terra), var(--terra-dark));
}
.result-card::after {
    content: "";
    position: absolute;
    top: 3px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 2px;
    background: var(--terra-light);
    border-radius: 2px;
    opacity: 0.5;
}
.result-card h3 {
    font-family: 'Cinzel', serif;
    color: var(--terra-light);
    margin-bottom: 0.8rem;
    font-size: 1.1rem;
    padding-top: 0.3rem;
}

/* ── Word-count badge ────────────────────────────────────────── */
.word-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: linear-gradient(135deg, var(--terra-dark), var(--terra));
    color: var(--cream);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.7rem;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Sidebar ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E1812 0%, var(--bg-primary) 100%);
    border-right: 1px solid var(--border-terra);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 0.5rem;
}

.sidebar-brand {
    text-align: center;
    padding: 1.5rem 1rem 0.8rem;
}
.sidebar-brand .brand-icon {
    font-size: 2.2rem;
    display: inline-block;
    animation: floatIcon 3s ease-in-out infinite;
    margin-bottom: 0.3rem;
}
.sidebar-brand h2 {
    font-family: 'Cinzel', serif;
    font-size: 1.15rem;
    font-weight: 600;
    background: linear-gradient(135deg, var(--cream), var(--terra-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
    letter-spacing: 0.5px;
}
.sidebar-brand .version {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    color: var(--text-muted);
    background: rgba(196,105,61,0.08);
    padding: 3px 12px;
    border-radius: 20px;
    border: 1px solid rgba(196,105,61,0.15);
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* status indicator */
.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.6rem 0.8rem;
    border-radius: var(--radius-sm);
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.5rem 0;
    transition: all var(--transition);
}
.status-indicator.active {
    background: rgba(107, 142, 90, 0.1);
    border: 1px solid rgba(107, 142, 90, 0.2);
    color: #8FB87A;
}
.status-indicator.error {
    background: rgba(196, 93, 74, 0.1);
    border: 1px solid rgba(196, 93, 74, 0.2);
    color: #D4806E;
}
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
}
.status-dot.active  { background: #6B8E5A; box-shadow: 0 0 6px #6B8E5A; }
.status-dot.error   { background: #C45D4A; box-shadow: 0 0 6px #C45D4A; }

/* fact card */
.fact-card {
    background: rgba(196,105,61,0.05);
    border: 1px solid rgba(196,105,61,0.12);
    border-left: 3px solid var(--terra);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 0.9rem 1rem;
    margin: 0.6rem 0;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.6;
    font-style: italic;
}

/* sidebar info list */
.sidebar-info {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: var(--text-muted);
    padding: 0.5rem 0;
}
.sidebar-info .info-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(196,105,61,0.06);
}
.sidebar-info .info-item:last-child {
    border-bottom: none;
}
.sidebar-info .info-icon {
    font-size: 0.85rem;
    width: 20px;
    text-align: center;
}

/* ── Streamlit element tweaks ────────────────────────────────── */
.stAlert > div { border-radius: var(--radius-md) !important; }
.stSpinner > div { border-color: var(--terra) !important; }
.stImage {
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-soft);
    border: 1px solid var(--border-terra);
}
h1, h2, h3, h4 { font-family: 'Inter', sans-serif; }
.stMarkdown {
    font-family: 'Inter', sans-serif;
    line-height: 1.7;
}
.stMarkdown a { color: var(--terra-light) !important; text-decoration: underline !important; text-underline-offset: 3px; }
.stMarkdown a:hover { color: var(--terra) !important; }

/* expander styling */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: 1px solid var(--border-terra) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Footer ──────────────────────────────────────────────────── */
.app-footer {
    text-align: center;
    padding: 1.5rem 0 1rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}
.app-footer span { color: var(--terra-light); font-weight: 500; }
.app-footer .footer-links {
    margin-top: 0.4rem;
    font-size: 0.7rem;
    opacity: 0.6;
}

/* ── Helper text styling ─────────────────────────────────────── */
.helper-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Image preview container ─────────────────────────────────── */
.img-preview-container {
    display: flex;
    justify-content: center;
    padding: 1rem 0;
    animation: fadeIn 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ─── API Configuration ────────────────────────────────────────────────────────
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

api_key = "AIzaSyAnLAkep1HMjzG5tr-u-_sDF5sjoqYeF_o"
try:
    genai.configure(api_key=api_key)
    st.session_state.api_key_configured = True
except Exception as e:
    st.session_state.api_key_configured = False

# ─── Historical facts ─────────────────────────────────────────────────────────
HISTORICAL_FACTS = [
    "The Great Pyramid of Giza was the tallest man-made structure for 3,800 years.",
    "Leonardo da Vinci wrote most of his notes in mirror script — backward writing.",
    "The Rosetta Stone was the key to deciphering Egyptian hieroglyphics.",
    "The Bayeux Tapestry is 70 meters long and depicts the Norman conquest of 1066.",
    "Tutankhamun's tomb contained over 5,000 artifacts when discovered in 1922.",
    "The Colosseum in Rome could hold up to 50,000 spectators in ancient times.",
    "The Library of Alexandria held hundreds of thousands of scrolls from the ancient world.",
    "The Antikythera mechanism is the world's oldest known analog computer.",
    "Medieval knights' armor weighed up to 50 lbs but was evenly distributed.",
    "The Dead Sea Scrolls are among the oldest biblical manuscripts — 2,000 years old.",
]

# ─── Helper ────────────────────────────────────────────────────────────────────
def get_gemini_response(prompt, image=None):
    """Generate response from Gemini model."""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        if image:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">🏛️</div>
        <h2>Artifact Explorer</h2>
        <span class="version">v2.0 · Gemini AI</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    # API Status
    if st.session_state.api_key_configured:
        st.markdown(
            '<div class="status-indicator active">'
            '<span class="status-dot active"></span>'
            'Gemini API Connected</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-indicator error">'
            '<span class="status-dot error"></span>'
            'API Disconnected</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    # Random fact
    st.markdown('<div class="section-label">💡 Did You Know?</div>', unsafe_allow_html=True)
    fact = random.choice(HISTORICAL_FACTS)
    st.markdown(f'<div class="fact-card">{fact}</div>', unsafe_allow_html=True)

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    # Capabilities
    st.markdown('<div class="section-label">🔧 Capabilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info">
        <div class="info-item"><span class="info-icon">📝</span> Text-based artifact descriptions</div>
        <div class="info-item"><span class="info-icon">🖼️</span> Image-based artifact analysis</div>
        <div class="info-item"><span class="info-icon">📥</span> Downloadable research reports</div>
        <div class="info-item"><span class="info-icon">🎯</span> Adjustable detail level</div>
        <div class="info-item"><span class="info-icon">🤖</span> Powered by Gemini 2.5 Flash</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)

    with st.expander("ℹ️ About"):
        st.markdown("""
        Upload an image of any historical artifact or enter its name,
        and **Gemini 2.5 Flash** will generate a rich, detailed description
        covering its origin, significance, and modern context.
        
        Built for historians, museum curators, and history enthusiasts.
        """)

# ─── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-icon">🏛️</div>
    <h1>Historical Artifact Explorer</h1>
    <p class="subtitle">Uncover the stories behind humanity's greatest treasures — powered by Gemini AI</p>
</div>
<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>
""", unsafe_allow_html=True)

# ─── Main Tabs ────────────────────────────────────────────────────────────────
tab_text, tab_image = st.tabs(["✍️  Describe by Name", "🖼️  Analyze from Image"])

# ── Tab 1 — Text description ─────────────────────────────────────────────────
with tab_text:
    st.markdown("""
    <div class="glass-card">
        <h3>📝 Enter Artifact Details</h3>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-muted); margin: 0;">
            Type the name of any artifact, monument, or historical period to generate a detailed scholarly description.
        </p>
    </div>
    """, unsafe_allow_html=True)

    artifact_name = st.text_input(
        "Artifact name or historical period",
        placeholder="e.g., Tutankhamun's Golden Mask, Terracotta Army, Viking Runestone…",
        label_visibility="collapsed",
    )

    col_slider, col_badge = st.columns([4, 1])
    with col_slider:
        word_count = st.slider(
            "Description length (words)",
            min_value=500, max_value=2000, value=1000, step=100,
        )
    with col_badge:
        st.markdown("")  # spacing
        st.markdown(
            f'<div style="padding-top: 1.8rem;"><span class="word-badge">≈ {word_count} words</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")  # spacer

    if st.button("🚀 Generate Description", key="btn_text", use_container_width=True):
        if not st.session_state.api_key_configured:
            st.error("⚠️ API key is not configured. Check the sidebar for status.")
        elif not artifact_name.strip():
            st.warning("Please enter an artifact name or historical period first.")
        else:
            with st.spinner("🔮 Gemini is researching the archives…"):
                prompt = f"""Generate a detailed and engaging description of **{artifact_name}**.

Include the following sections:
1. **Historical Background** — Origin, time period, cultural context
2. **Physical Characteristics** — Materials, dimensions, notable features
3. **Historical Significance** — Importance and lasting impact
4. **Interesting Facts** — Unique or lesser-known details
5. **Modern Context** — Relevance today and current location

Write approximately {word_count} words in an engaging, informative tone suitable for historians, museum curators, and history enthusiasts. Use markdown formatting with headers."""

                response = get_gemini_response(prompt)

            # Result
            st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)
            word_ct = len(response.split())
            st.markdown(
                f'<div class="result-card">'
                f'<h3>📚 {artifact_name}</h3>'
                f'<span class="word-badge">{word_ct} words</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown(response)

            st.markdown("")  # spacer
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.download_button(
                    "📥 Download as Text",
                    data=response,
                    file_name=f"{artifact_name.replace(' ', '_')}_description.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with col_b:
                st.download_button(
                    "📋 Download as Markdown",
                    data=response,
                    file_name=f"{artifact_name.replace(' ', '_')}_description.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

# ── Tab 2 — Image analysis ───────────────────────────────────────────────────
with tab_image:
    st.markdown("""
    <div class="glass-card">
        <h3>🖼️ Upload an Artifact Image</h3>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-muted); margin: 0;">
            Upload a photo of any artifact — pottery, sculpture, manuscript, weapon, jewelry, architecture — for AI-powered analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drag and drop or browse — JPG, PNG, GIF, WEBP",
        type=["jpg", "jpeg", "png", "gif", "webp"],
        label_visibility="collapsed",
    )

    col_slider2, col_badge2 = st.columns([4, 1])
    with col_slider2:
        img_word_count = st.slider(
            "Analysis length (words)",
            min_value=500, max_value=2000, value=1000, step=100,
            key="img_slider",
        )
    with col_badge2:
        st.markdown("")
        st.markdown(
            f'<div style="padding-top: 1.8rem;"><span class="word-badge">≈ {img_word_count} words</span></div>',
            unsafe_allow_html=True,
        )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            st.image(image, caption="📷 Uploaded Artifact", width=300)

    st.markdown("")  # spacer

    if st.button("🔍 Analyze Artifact", key="btn_img", use_container_width=True):
        if not st.session_state.api_key_configured:
            st.error("⚠️ API key is not configured. Check the sidebar for status.")
        elif uploaded_file is None:
            st.warning("Please upload an image of the artifact first.")
        else:
            with st.spinner("🔮 Gemini is examining the artifact…"):
                image_parts = {
                    "mime_type": uploaded_file.type,
                    "data": uploaded_file.getvalue(),
                }
                prompt = f"""You are a world-class historian and artifact expert.
Analyze the artifact shown in this image and provide a detailed description.

Include:
1. **Identification** — What is this artifact? Classify its type and likely origin.
2. **Historical Background** — Period, culture, and context.
3. **Physical Analysis** — Materials, craftsmanship, condition.
4. **Significance** — Why is it important?
5. **Interesting Facts** — Unique details.

Write approximately {img_word_count} words in an engaging, scholarly tone. Use markdown formatting with headers."""

                response = get_gemini_response(prompt, image_parts)

            st.markdown('<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>', unsafe_allow_html=True)
            word_ct = len(response.split())
            st.markdown(
                f'<div class="result-card">'
                f'<h3>🔎 Artifact Analysis</h3>'
                f'<span class="word-badge">{word_ct} words</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown(response)

            st.markdown("")  # spacer
            col_dl1, col_dl2 = st.columns([1, 1])
            with col_dl1:
                st.download_button(
                    "📥 Download Analysis",
                    data=response,
                    file_name="artifact_analysis.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with col_dl2:
                st.download_button(
                    "📋 Download as Markdown",
                    data=response,
                    file_name="artifact_analysis.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ornament-divider"><div class="line"></div><div class="diamond"></div><div class="line"></div></div>
<div class="app-footer">
    Powered by <span>Google Gemini 2.5 Flash</span> · Built for Historical Research<br>
    <div class="footer-links">Crafted with care for historians & museum curators</div>
</div>
""", unsafe_allow_html=True)
>>>>>>> ab57571598dda2b24b1c97c89131ec93ce66ac0d:Gemini Historical Artifact/app.py

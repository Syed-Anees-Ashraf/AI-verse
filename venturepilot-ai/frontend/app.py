import streamlit as st
import requests

API_BASE_URL = "http://localhost:8080/api"

st.set_page_config(page_title="VenturePilot AI", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# ==================== CLEAN MODERN CSS ====================
st.markdown("""
<style>
/* Import Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Reset & Base */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
.stApp { background: #EBE1D1 !important; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }
* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }

/* Hide Streamlit defaults */
#MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] { display: none !important; }

/* ===== NAVBAR ===== */
.navbar {
    background: #FFFFFF;
    padding: 16px 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #41644A;
    position: sticky;
    top: 0;
    z-index: 1000;
}
.nav-left {
    display: flex;
    align-items: center;
    gap: 40px;
}
.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.logo-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #41644A 0%, #0D4715 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
}
.logo-text {
    font-size: 20px;
    font-weight: 700;
    color: #000000;
}
.nav-links {
    display: flex;
    gap: 32px;
}
.nav-link {
    font-size: 15px;
    font-weight: 500;
    color: #000000;
    text-decoration: none;
    transition: color 0.2s;
    cursor: pointer;
}
.nav-link:hover, .nav-link.active {
    color: #0D4715;
}
.nav-right {
    display: flex;
    align-items: center;
    gap: 16px;
}
.status-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: #41644A;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 500;
    color: #FFFFFF;
}
.status-dot {
    width: 8px;
    height: 8px;
    background: #22C55E;
    border-radius: 50%;
}
.btn-primary {
    background: linear-gradient(135deg, #41644A 0%, #0D4715 100%);
    color: white !important;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
    border: none;
}
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(65, 100, 74, 0.3);
}

/* ===== HERO SECTION ===== */
.hero {
    padding: 80px 48px;
    max-width: 1280px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 64px;
    align-items: center;
}
.hero-content {
    max-width: 560px;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #E9762B;
    color: #FFFFFF;
    padding: 8px 16px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 24px;
}
.hero-title {
    font-size: 56px;
    font-weight: 800;
    color: #000000;
    line-height: 1.1;
    margin-bottom: 24px;
}
.hero-title span {
    color: #41644A;
}
.hero-desc {
    font-size: 18px;
    color: #000000;
    line-height: 1.7;
    margin-bottom: 32px;
}
.hero-buttons {
    display: flex;
    gap: 16px;
}
.btn-secondary {
    background: #FFFFFF;
    color: #000000 !important;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    border: 1px solid #41644A;
    cursor: pointer;
    transition: all 0.2s;
}
.btn-secondary:hover {
    background: #EBE1D1;
    border-color: #0D4715;
}
.btn-large {
    padding: 14px 28px;
    font-size: 16px;
}

/* Hero Visual Card */
.hero-visual {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
    border: 1px solid #41644A;
}
.visual-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}
.visual-title {
    font-size: 14px;
    font-weight: 600;
    color: #000000;
}
.visual-badge {
    background: #41644A;
    color: #FFFFFF;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 600;
}
.stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
.stat-box {
    background: #EBE1D1;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
}
.stat-value {
    font-size: 36px;
    font-weight: 800;
    color: #000000;
    margin-bottom: 4px;
}
.stat-value.purple { color: #0D4715; }
.stat-value.green { color: #41644A; }
.stat-value.orange { color: #E9762B; }
.stat-label {
    font-size: 13px;
    color: #000000;
    font-weight: 500;
}

/* ===== TRUSTED BY ===== */
.trusted {
    padding: 40px 48px;
    background: #FFFFFF;
    border-top: 1px solid #41644A;
    border-bottom: 1px solid #41644A;
}
.trusted-inner {
    max-width: 1280px;
    margin: 0 auto;
    text-align: center;
}
.trusted-text {
    font-size: 14px;
    color: #000000;
    font-weight: 500;
    margin-bottom: 24px;
}
.trusted-logos {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 48px;
    flex-wrap: wrap;
}
.trusted-logo {
    font-size: 20px;
    font-weight: 700;
    color: #000000;
}

/* ===== FEATURES SECTION ===== */
.features {
    padding: 96px 48px;
    max-width: 1280px;
    margin: 0 auto;
}
.section-header {
    text-align: center;
    max-width: 640px;
    margin: 0 auto 64px;
}
.section-badge {
    display: inline-block;
    background: #E9762B;
    color: #FFFFFF;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 16px;
}
.section-title {
    font-size: 40px;
    font-weight: 800;
    color: #000000;
    margin-bottom: 16px;
}
.section-desc {
    font-size: 18px;
    color: #000000;
    line-height: 1.6;
}
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
}
.feature-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 32px;
    border: 1px solid #41644A;
    transition: all 0.3s ease;
}
.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    border-color: #0D4715;
}
.feature-card.featured {
    background: linear-gradient(135deg, #41644A 0%, #0D4715 100%);
    border: none;
    grid-row: span 2;
}
.feature-card.featured * {
    color: white !important;
}
.feature-card.featured .feature-icon {
    background: rgba(255,255,255,0.2);
}
.feature-icon {
    width: 56px;
    height: 56px;
    background: #EBE1D1;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin-bottom: 20px;
}
.feature-title {
    font-size: 20px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 12px;
}
.feature-desc {
    font-size: 15px;
    color: #000000;
    line-height: 1.6;
}

/* ===== NEWS SECTION ===== */
.news {
    padding: 64px 48px;
    background: #FFFFFF;
}
.news-inner {
    max-width: 1280px;
    margin: 0 auto;
}
.news-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
}
.news-title {
    font-size: 24px;
    font-weight: 700;
    color: #000000;
}
.news-live {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #E9762B;
    color: #FFFFFF;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 600;
}
.news-dot {
    width: 6px;
    height: 6px;
    background: #FFFFFF;
    border-radius: 50%;
    animation: blink 1s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.news-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}
.news-card {
    background: #EBE1D1;
    border-radius: 16px;
    padding: 24px;
    transition: all 0.2s;
}
.news-card:hover {
    background: #FFFFFF;
}
.news-cat {
    font-size: 11px;
    font-weight: 700;
    color: #E9762B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}
.news-text {
    font-size: 15px;
    font-weight: 600;
    color: #000000;
    line-height: 1.5;
    margin-bottom: 12px;
}
.news-time {
    font-size: 13px;
    color: #000000;
}

/* ===== FORM PAGE ===== */
.form-page {
    padding: 64px 48px;
    max-width: 720px;
    margin: 0 auto;
}
.form-card {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08);
    border: 1px solid #E5E7EB;
}
.form-header {
    text-align: center;
    margin-bottom: 40px;
}
.form-title {
    font-size: 32px;
    font-weight: 800;
    color: #000000;
    margin-bottom: 8px;
}
.form-subtitle {
    font-size: 16px;
    color: #000000;
}
.form-group {
    margin-bottom: 24px;
}
.form-label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
}

/* ===== DASHBOARD ===== */
.dashboard {
    padding: 48px;
    max-width: 1280px;
    margin: 0 auto;
}
.dash-header {
    margin-bottom: 32px;
}
.dash-title {
    font-size: 28px;
    font-weight: 800;
    color: #000000;
    margin-bottom: 12px;
}
.dash-tags {
    display: flex;
    gap: 12px;
}
.dash-tag {
    background: #E9762B;
    color: #FFFFFF;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
}
.dash-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
    margin-bottom: 32px;
}
.dash-stat {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #41644A;
}
.dash-stat-label {
    font-size: 13px;
    color: #000000;
    font-weight: 500;
    margin-bottom: 8px;
}
.dash-stat-value {
    font-size: 28px;
    font-weight: 800;
    color: #000000;
}
.dash-stat-value.success { color: #41644A; }
.dash-stat-value.warning { color: #E9762B; }
.dash-stat-value.purple { color: #0D4715; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 6px;
    gap: 4px;
    border: 1px solid #41644A;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    color: #000000 !important;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #41644A 0%, #0D4715 100%) !important;
    color: white !important;
}

/* Content cards */
.content-section {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #E5E7EB;
    margin-top: 24px;
}
.content-title {
    font-size: 16px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ===== CHAT PAGE ===== */
.chat-page {
    padding: 48px;
    max-width: 900px;
    margin: 0 auto;
}
.chat-header {
    text-align: center;
    margin-bottom: 32px;
}
.chat-title {
    font-size: 28px;
    font-weight: 800;
    color: #000000;
    margin-bottom: 8px;
}
.chat-subtitle {
    font-size: 16px;
    color: #000000;
}
.chat-container {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 24px;
    min-height: 400px;
    border: 1px solid #41644A;
    margin-bottom: 24px;
}
.chat-empty {
    text-align: center;
    padding: 80px 20px;
}
.chat-empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
}
.chat-empty-text {
    font-size: 16px;
    color: #000000;
}
.chat-msg {
    margin-bottom: 16px;
    max-width: 75%;
}
.chat-msg.user {
    margin-left: auto;
    background: linear-gradient(135deg, #41644A 0%, #0D4715 100%);
    color: white;
    padding: 14px 20px;
    border-radius: 20px 20px 4px 20px;
}
.chat-msg.ai {
    background: #EBE1D1;
    color: #000000;
    padding: 14px 20px;
    border-radius: 20px 20px 20px 4px;
}
.quick-questions {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

/* Button overrides */
.stButton > button {
    background: linear-gradient(135deg, #41644A 0%, #0D4715 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.2s !important;
    font-size: 14px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(65, 100, 74, 0.3) !important;
}

/* Text overrides for visibility */
.stMarkdown, .stMarkdown p, .stMarkdown div {
    color: #000000 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #000000 !important;
}
.stText, .stText > div {
    color: #000000 !important;
}

/* Input overrides */
.stTextArea textarea, .stTextInput input {
    background: #FFFFFF !important;
    border: 2px solid #41644A !important;
    border-radius: 12px !important;
    padding: 14px !important;
    font-size: 15px !important;
    color: #000000 !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #0D4715 !important;
    box-shadow: 0 0 0 3px rgba(65, 100, 74, 0.1) !important;
}
.stSelectbox > div > div {
    background: #FFFFFF !important;
    border: 2px solid #41644A !important;
    border-radius: 12px !important;
}
.stSelectbox > div > div > div {
    color: #000000 !important;
}

/* Alerts */
.stSuccess { background: #41644A !important; color: #FFFFFF !important; border-left: 4px solid #0D4715 !important; border-radius: 8px !important; }
.stInfo { background: #E9762B !important; color: #FFFFFF !important; border-left: 4px solid #000000 !important; border-radius: 8px !important; }
.stWarning { background: #EBE1D1 !important; color: #000000 !important; border-left: 4px solid #E9762B !important; border-radius: 8px !important; }
.stError { background: #E9762B !important; color: #FFFFFF !important; border-left: 4px solid #000000 !important; border-radius: 8px !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #FFFFFF !important;
    border: 1px solid #41644A !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    color: #000000 !important;
}
.streamlit-expanderContent {
    background: #FFFFFF !important;
    color: #000000 !important;
}

/* Form labels and text */
label, .stFormLabel {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Ensure all text elements are visible */
div[data-testid="stMarkdownContainer"] p {
    color: #000000 !important;
}
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4 {
    color: #000000 !important;
}

/* Fix any remaining invisible text */
.stApp, .stApp * {
    color: inherit;
}
.stApp p, .stApp div, .stApp span {
    color: #000000 !important;
}
.stApp strong, .stApp b {
    color: #000000 !important;
}

/* Placeholder text */
input::placeholder, textarea::placeholder {
    color: #000000 !important;
    opacity: 0.6;
}

/* Spinner and loading text */
.stSpinner > div {
    color: #41644A !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 48px;
    border-top: 1px solid #41644A;
    margin-top: 64px;
}
.footer-text {
    font-size: 14px;
    color: #000000;
}
.footer-brand {
    font-weight: 700;
    color: #41644A;
}
</style>
""", unsafe_allow_html=True)

# ==================== API FUNCTIONS ====================
def init_session_state():
    defaults = {'startup_profile': None, 'analysis_results': None, 'chat_history': [], 'current_page': 'home'}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def check_api():
    try:
        return requests.get("http://localhost:8080/health", timeout=2).status_code == 200
    except:
        return False

def api_onboard(data):
    try:
        r = requests.post(f"{API_BASE_URL}/onboard", json=data, timeout=60)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def api_dashboard(profile):
    try:
        r = requests.post(f"{API_BASE_URL}/dashboard", json=profile, timeout=120)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def api_chat(q, profile):
    try:
        r = requests.post(f"{API_BASE_URL}/chat", json={"question": q, "startup_profile": profile, "conversation_history": st.session_state.chat_history[-10:]}, timeout=60)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# ==================== COMPONENTS ====================
def render_navbar():
    online = check_api()
    st.markdown(f'''
    <div class="navbar">
        <div class="nav-left">
            <div class="logo">
                <div class="logo-icon">🚀</div>
                <div class="logo-text">VenturePilot</div>
            </div>
        </div>
        <div class="nav-right">
            <div class="status-pill">
                <div class="status-dot" style="background: {'#22C55E' if online else '#EF4444'};"></div>
                {'Online' if online else 'Offline'}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Navigation buttons
    cols = st.columns([1,1,1,1,4])
    with cols[0]:
        if st.button("🏠 Home", key="n1", use_container_width=True):
            st.session_state.current_page = 'home'; st.rerun()
    with cols[1]:
        if st.button("✨ Analyze", key="n2", use_container_width=True):
            st.session_state.current_page = 'onboarding'; st.rerun()
    with cols[2]:
        if st.session_state.analysis_results:
            if st.button("📊 Dashboard", key="n3", use_container_width=True):
                st.session_state.current_page = 'dashboard'; st.rerun()
    with cols[3]:
        if st.session_state.startup_profile:
            if st.button("💬 Chat", key="n4", use_container_width=True):
                st.session_state.current_page = 'chat'; st.rerun()

# ==================== PAGES ====================
def page_home():
    # Hero Section
    col1, col2 = st.columns([1.1, 1], gap="large")
    
    with col1:
        st.markdown('''
        <div style="padding: 60px 48px;">
            <div class="hero-badge">🤖 AI-Powered Platform</div>
            <h1 class="hero-title">Take your <span>startup</span> to another level</h1>
            <p class="hero-desc">Get intelligent investor matching, policy insights, market analysis, and strategic recommendations — all powered by 6 specialized AI agents.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        c1, c2, _ = st.columns([1, 1, 2])
        with c1:
            if st.button("🚀 Get Started", key="cta1", use_container_width=True):
                st.session_state.current_page = 'onboarding'; st.rerun()
    
    with col2:
        st.markdown('''
        <div class="hero-visual" style="margin: 40px 48px 40px 0;">
            <div class="visual-header">
                <div class="visual-title">Platform Statistics</div>
                <div class="visual-badge">Live</div>
            </div>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-value purple">500+</div>
                    <div class="stat-label">Investors Database</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value green">50+</div>
                    <div class="stat-label">Policy Schemes</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value orange">6</div>
                    <div class="stat-label">AI Agents</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">24/7</div>
                    <div class="stat-label">Availability</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Trusted By
    st.markdown('''
    <div class="trusted">
        <div class="trusted-inner">
            <div class="trusted-text">Trusted by startups backed by</div>
            <div class="trusted-logos">
                <span class="trusted-logo">Y Combinator</span>
                <span class="trusted-logo">Sequoia</span>
                <span class="trusted-logo">Accel</span>
                <span class="trusted-logo">a16z</span>
                <span class="trusted-logo">Tiger Global</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Features Section
    st.markdown('''
    <div class="features">
        <div class="section-header">
            <div class="section-badge">Features</div>
            <h2 class="section-title">Everything you need to scale</h2>
            <p class="section-desc">Our AI agents work together to give you comprehensive insights for your startup journey.</p>
        </div>
        <div class="features-grid">
            <div class="feature-card featured">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Smart Investor Matching</div>
                <div class="feature-desc">Our AI analyzes your startup profile and matches you with the most relevant investors based on domain expertise, stage preference, geography, and past investments. Get detailed reasoning for each match.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">Policy Intelligence</div>
                <div class="feature-desc">Discover government schemes, grants, tax benefits, and regulatory requirements specific to your industry.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Market Analysis</div>
                <div class="feature-desc">Get market sizing, growth signals, competitive landscape, and emerging trends for your sector.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Strategy Synthesis</div>
                <div class="feature-desc">Receive actionable recommendations synthesized from all AI agents combined.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">AI Chat Assistant</div>
                <div class="feature-desc">Ask questions and get contextual answers about your startup, market, and investors.</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # News Section
    news = [
        {"cat": "FUNDING", "text": "AI startups raised record $50B in 2024", "time": "2 hours ago"},
        {"cat": "POLICY", "text": "New startup tax benefits announced in India", "time": "5 hours ago"},
        {"cat": "MARKET", "text": "SaaS market projected to reach $900B by 2028", "time": "8 hours ago"},
        {"cat": "VC NEWS", "text": "Sequoia launches new $2.5B AI-focused fund", "time": "1 day ago"},
    ]
    
    st.markdown('''
    <div class="news">
        <div class="news-inner">
            <div class="news-header">
                <div class="news-title">📡 Latest Startup News</div>
                <div class="news-live"><div class="news-dot"></div>LIVE</div>
            </div>
            <div class="news-grid">
    ''', unsafe_allow_html=True)
    
    for n in news:
        st.markdown(f'''
            <div class="news-card">
                <div class="news-cat">{n['cat']}</div>
                <div class="news-text">{n['text']}</div>
                <div class="news-time">{n['time']}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div></div></div>', unsafe_allow_html=True)

def page_onboarding():
    st.markdown('<div class="form-page">', unsafe_allow_html=True)
    st.markdown('''
    <div class="form-card">
        <div class="form-header">
            <div class="form-title">Tell us about your startup</div>
            <div class="form-subtitle">Our AI will analyze and find the best opportunities for you</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form("startup_form"):
        st.markdown("**📝 Startup Description**")
        desc = st.text_area("Description", placeholder="What problem are you solving? Who are your customers? What makes you unique?", height=140, label_visibility="collapsed", help="Provide a detailed description of your startup")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**🏢 Domain**")
            domain = st.selectbox("Domain", ["Fintech", "Healthtech", "EdTech", "SaaS", "AI/ML", "E-commerce", "Logistics", "AgriTech", "CleanTech", "Other"], label_visibility="collapsed")
            st.markdown("**🌍 Geography**")
            geo = st.selectbox("Geography", ["India", "USA", "UK", "Singapore", "UAE", "Global"], label_visibility="collapsed")
        with c2:
            st.markdown("**📊 Stage**")
            stage = st.selectbox("Stage", ["Idea", "Pre-seed", "Seed", "Series A", "Series B", "Growth"], label_visibility="collapsed")
            st.markdown("**👥 Customer Type**")
            cust = st.selectbox("Customer", ["B2B", "B2C", "B2B2C", "D2C", "Marketplace", "Enterprise"], label_visibility="collapsed")
        
        if st.form_submit_button("🚀 Analyze My Startup", use_container_width=True):
            if len(desc) < 20:
                st.error("Please provide a more detailed description (at least 20 characters)")
            else:
                with st.spinner("🤖 AI agents analyzing..."):
                    result = api_onboard({"description": desc, "domain": domain, "stage": stage, "geography": geo, "customer_type": cust})
                    if result:
                        st.session_state.startup_profile = result
                        with st.spinner("📊 Running full analysis..."):
                            dash = api_dashboard(result)
                            if dash:
                                st.session_state.analysis_results = dash
                                st.session_state.current_page = 'dashboard'
                                st.rerun()
                    else:
                        st.error("Analysis failed. Check if API is running.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def page_dashboard():
    results = st.session_state.analysis_results
    profile = st.session_state.startup_profile
    if not results:
        st.warning("No results. Please analyze your startup first.")
        return
    
    st.markdown('<div class="dashboard">', unsafe_allow_html=True)
    
    # Header
    st.markdown(f'''
    <div class="dash-header">
        <div class="dash-title">📊 Analysis Dashboard</div>
        <div class="dash-tags">
            <span class="dash-tag">{profile.get('domain', '')}</span>
            <span class="dash-tag">{profile.get('stage', '')} Stage</span>
            <span class="dash-tag">{profile.get('geography', '')}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    strategy = results.get('strategy', {})
    investors = results.get('investors', [])
    market = results.get('market', {})
    readiness = strategy.get('fundraising_readiness', 'medium')
    
    # Stats
    c1, c2, c3, c4 = st.columns(4)
    colors = {'high': 'success', 'medium': 'warning', 'low': ''}
    with c1:
        st.markdown(f'<div class="dash-stat"><div class="dash-stat-label">Fundraising Readiness</div><div class="dash-stat-value {colors.get(readiness, "")}" style="text-transform:uppercase;">{readiness}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="dash-stat"><div class="dash-stat-label">Matched Investors</div><div class="dash-stat-value purple">{len(investors)}</div></div>', unsafe_allow_html=True)
    with c3:
        score = investors[0].get('match_score', 0) if investors else 0
        st.markdown(f'<div class="dash-stat"><div class="dash-stat-label">Top Match Score</div><div class="dash-stat-value">{score}%</div></div>', unsafe_allow_html=True)
    with c4:
        mkt = market.get('market_size_estimate', 'N/A')[:20]
        st.markdown(f'<div class="dash-stat"><div class="dash-stat-label">Market Size</div><div class="dash-stat-value" style="font-size:18px;">{mkt}</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    t1, t2, t3, t4, t5 = st.tabs(["💰 Investors", "📋 Policy", "📈 Market", "📰 News", "🎯 Strategy"])
    
    with t1:
        if not investors:
            st.info("No investors matched.")
        else:
            for i, inv in enumerate(investors[:8]):
                with st.expander(f"**{inv.get('name', 'Unknown')}** — {inv.get('match_score', 0)}% Match", expanded=i<3):
                    st.write(f"**Why?** {inv.get('reason', 'N/A')}")
                    past = inv.get('past_investments', [])
                    if past: st.write(f"**Past:** {', '.join(past[:5])}")
    
    with t2:
        policy = results.get('policy', {})
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**✓ Relevant Policies**")
            for p in policy.get('relevant_policies', []): st.write(f"• {p}")
            st.markdown("**🎯 Eligible Schemes**")
            for s in policy.get('eligible_schemes', []): st.success(s)
        with c2:
            st.markdown("**⚠️ Regulatory Risks**")
            for r in policy.get('regulatory_risks', []): st.warning(r)
    
    with t3:
        st.write(f"**Market Size:** {market.get('market_size_estimate', 'N/A')}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**📈 Growth Signals**")
            for s in market.get('growth_signals', []): st.success(s)
        with c2:
            st.markdown("**🔮 Trends**")
            for t in market.get('emerging_trends', []): st.info(t)
        with c3:
            st.markdown("**⚠️ Risks**")
            for r in market.get('saturation_risks', []): st.warning(r)
    
    with t4:
        news = results.get('news', {})
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**✨ Opportunities**")
            for o in news.get('opportunities', []): st.success(o)
        with c2:
            st.markdown("**⚠️ Risks**")
            for r in news.get('risks', []): st.warning(r)
    
    with t5:
        icons = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}
        msgs = {'high': 'Well-positioned to raise!', 'medium': 'Some preparation needed.', 'low': 'Focus on traction first.'}
        st.markdown(f"""
        <div style="background:#EEF2FF;border-radius:16px;padding:32px;text-align:center;margin-bottom:24px;">
            <div style="font-size:48px;">{icons.get(readiness, '🟡')}</div>
            <div style="font-size:20px;font-weight:700;color:#111827;text-transform:uppercase;">Readiness: {readiness}</div>
            <div style="color:#6B7280;">{msgs.get(readiness, '')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**💡 Recommendations**")
            for i, r in enumerate(strategy.get('key_recommendations', []), 1): st.info(f"**{i}.** {r}")
        with c2:
            st.markdown("**✅ Next Actions**")
            for i, a in enumerate(strategy.get('next_actions', []), 1): st.write(f"**Step {i}:** {a}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def page_chat():
    profile = st.session_state.startup_profile
    if not profile:
        st.warning("Please analyze your startup first.")
        return
    
    st.markdown('''
    <div class="chat-page">
        <div class="chat-header">
            <div class="chat-title">💬 Chat with VenturePilot AI</div>
            <div class="chat-subtitle">Ask anything about investors, policies, market, or strategy</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown('''
        <div class="chat-empty">
            <div class="chat-empty-icon">💬</div>
            <div class="chat-empty-text">Start a conversation using the questions below</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            cls = "user" if msg['role'] == 'user' else "ai"
            st.markdown(f'<div class="chat-msg {cls}">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick questions
    st.markdown("**Quick Questions**")
    q1, q2, q3, q4 = st.columns(4)
    qs = [("🎯 Investors", "Who are the best investors for my startup?"),
          ("📋 Regulations", "What regulations should I know?"),
          ("💰 Schemes", "What schemes am I eligible for?"),
          ("📈 Market", "What's my market size?")]
    for col, (lbl, q) in zip([q1,q2,q3,q4], qs):
        with col:
            if st.button(lbl, key=f"q_{lbl}", use_container_width=True):
                st.session_state.chat_history.append({'role': 'user', 'content': q})
                with st.spinner("Thinking..."):
                    r = api_chat(q, profile)
                    if r: st.session_state.chat_history.append({'role': 'assistant', 'content': r.get('answer', 'Error')})
                st.rerun()
    
    # Input
    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_q = st.text_input("Message", placeholder="Type your question...", label_visibility="collapsed")
        with c2:
            if st.form_submit_button("Send", use_container_width=True) and user_q:
                st.session_state.chat_history.append({'role': 'user', 'content': user_q})
                with st.spinner("Thinking..."):
                    r = api_chat(user_q, profile)
                    if r: st.session_state.chat_history.append({'role': 'assistant', 'content': r.get('answer', 'Error')})
                st.rerun()
    
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []; st.rerun()

# ==================== MAIN ====================
def main():
    init_session_state()
    render_navbar()
    
    page = st.session_state.current_page
    if page == 'home': page_home()
    elif page == 'onboarding': page_onboarding()
    elif page == 'dashboard': page_dashboard()
    elif page == 'chat': page_chat()
    else: page_home()
    
    # Footer
    st.markdown('''
    <div class="footer">
        <div class="footer-text">
            <span class="footer-brand">VenturePilot AI</span> • Powered by Mistral AI
        </div>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

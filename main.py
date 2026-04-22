import streamlit as st
import requests
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title='Leaf Disease Detection',
    layout='wide',
    page_icon='🌿',
    initial_sidebar_state='collapsed'
)

# ================= LANGUAGE =================
if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

lang_map = {
    'English': {'code': 'en', 'flag': '🇬🇧 English'},
    'বাংলা':   {'code': 'bn', 'flag': '🇧🇩 বাংলা'},
}

def tr(text):
    try:
        code = lang_map[st.session_state.lang]['code']
        if code == 'en':
            return text
        return GoogleTranslator(source='auto', target=code).translate(text)
    except Exception:
        return text

# ================= STYLES =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfeff 50%, #f0f9ff 100%);
}
#MainMenu, footer, header {visibility: hidden;}

.hero {
    text-align:center;
    padding: 30px 20px 10px;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg,#16a34a,#0891b2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
}
.hero p {
    color:#475569;
    font-size: 1.05rem;
    margin: 0;
}

.card {
    background: #ffffff;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(2,132,199,0.08);
    border: 1px solid #e2e8f0;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 14px;
    display:flex; align-items:center; gap:8px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #f1f5f9;
    padding: 6px;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
    color: #475569;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg,#16a34a,#0891b2) !important;
    color: white !important;
}

.stButton > button {
    background: linear-gradient(90deg,#16a34a,#0891b2);
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1rem;
    width: 100%;
    transition: all .2s ease;
    box-shadow: 0 6px 18px rgba(22,163,74,0.25);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(22,163,74,0.35);
}

.empty-state {
    text-align:center;
    padding: 50px 20px;
    color:#64748b;
}
.empty-state .icon { font-size: 3.5rem; margin-bottom: 10px; }

.report-section {
    background: #f8fafc;
    border-left: 4px solid #16a34a;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
}
.report-section .label {
    font-size: .8rem;
    font-weight: 700;
    color: #16a34a;
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-bottom: 6px;
}
.report-section .value {
    font-size: 1rem;
    color: #0f172a;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ================= LANGUAGE SWITCHER =================
top_l, top_r = st.columns([6,1])
with top_r:
    selected = st.selectbox(
        "Lang",
        options=list(lang_map.keys()),
        index=list(lang_map.keys()).index(st.session_state.lang),
        format_func=lambda k: lang_map[k]['flag'],
        label_visibility="collapsed",
    )
    if selected != st.session_state.lang:
        st.session_state.lang = selected
        st.rerun()

# ================= HERO =================
st.markdown(f"""
<div class="hero">
    <h1>🌿 {tr("Leaf Disease Detection")}</h1>
    <p>{tr("AI-powered plant health analysis in seconds")}</p>
</div>
""", unsafe_allow_html=True)

# ================= MAIN LAYOUT =================
col1, col2 = st.columns([1, 1.2], gap="large")

# ---------- LEFT: INPUT ----------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📥 {tr("Provide a Leaf Image")}</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs([f"📁 {tr('Upload')}", f"📷 {tr('Camera')}"])

    image_file = None
    with tab1:
        uploaded = st.file_uploader(
            tr("Choose an image"),
            type=['jpg', 'jpeg', 'png'],
            label_visibility="collapsed"
        )
        if uploaded is not None:
            image_file = uploaded

    with tab2:
        captured = st.camera_input(
            tr("Take a picture"),
            label_visibility="collapsed"
        )
        if captured is not None:
            image_file = captured

    if image_file is not None:
        st.image(image_file, caption=tr("Selected leaf"), use_container_width=True)
        detect_clicked = st.button(f"🔍 {tr('Detect Disease')}")
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div class="icon">🍃</div>
            <div><b>{tr("No image yet")}</b></div>
            <div style="font-size:.9rem;margin-top:6px;">
                {tr("Upload a file or use your camera to begin")}
            </div>
        </div>
        """, unsafe_allow_html=True)
        detect_clicked = False

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RIGHT: RESULT ----------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📊 {tr("Detection Report")}</div>', unsafe_allow_html=True)

    if image_file is not None and detect_clicked:
        with st.spinner(tr("Analyzing leaf...")):
            try:
                files = {"file": (image_file.name if hasattr(image_file, "name") else "capture.png",
                                  image_file.getvalue(),
                                  "image/png")}
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    files=files,
                    timeout=60
                )
            except requests.exceptions.RequestException:
                st.error(tr("Could not connect to the detection server."))
                response = None

        if response is not None and response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                for k, v in result.items():
                    st.markdown(f"""
                    <div class="report-section">
                        <div class="label">{tr(str(k))}</div>
                        <div class="value">{tr(str(v))}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="report-section">
                    <div class="label">{tr("Result")}</div>
                    <div class="value">{tr(str(result))}</div>
                </div>
                """, unsafe_allow_html=True)
        elif response is not None:
            st.error(f"{tr('API Error')}: {response.status_code}")
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div class="icon">📄</div>
            <div><b>{tr("Awaiting analysis")}</b></div>
            <div style="font-size:.9rem;margin-top:6px;">
                {tr("Provide an image and click Detect Disease")}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

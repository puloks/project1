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
    'हिन्दी':  {'code': 'hi', 'flag': '🇮🇳 हिन्दी'},
}

translations = {
    'English': {
        'title': 'Leaf Disease Detection',
        'desc': 'AI-powered plant health diagnosis. Upload a leaf image to get an instant report.',
        'upload': 'Drop a leaf image here',
        'detect': 'Analyze Leaf',
        'preview': 'Preview',
        'loading': 'Analyzing your leaf...',
        'upload_section': 'Upload',
        'analysis_section': 'Diagnosis',
        'empty': 'Upload a leaf image on the left to begin diagnosis.',
        'report': 'Detection Report',
        'badge': 'AI Powered',
    },
    'বাংলা': {
        'title': 'পাতার রোগ শনাক্তকরণ',
        'desc': 'এআই দিয়ে গাছের স্বাস্থ্য পরীক্ষা। পাতার ছবি আপলোড করে সাথে সাথে রিপোর্ট নিন।',
        'upload': 'এখানে পাতার ছবি দিন',
        'detect': 'পাতা বিশ্লেষণ করুন',
        'preview': 'প্রিভিউ',
        'loading': 'আপনার পাতা বিশ্লেষণ চলছে...',
        'upload_section': 'আপলোড',
        'analysis_section': 'নির্ণয়',
        'empty': 'শুরু করতে বাঁ পাশে একটি পাতার ছবি আপলোড করুন।',
        'report': 'শনাক্তকরণ রিপোর্ট',
        'badge': 'এআই চালিত',
    },
    'हिन्दी': {
        'title': 'पत्ती रोग पहचान',
        'desc': 'एआई आधारित पौधा स्वास्थ्य जांच। पत्ती की फोटो अपलोड कर तुरंत रिपोर्ट पाएं।',
        'upload': 'पत्ती की फोटो यहाँ डालें',
        'detect': 'पत्ती की जांच करें',
        'preview': 'पूर्वावलोकन',
        'loading': 'आपकी पत्ती की जांच हो रही है...',
        'upload_section': 'अपलोड',
        'analysis_section': 'निदान',
        'empty': 'शुरू करने के लिए बाईं ओर एक पत्ती की फोटो अपलोड करें।',
        'report': 'पहचान रिपोर्ट',
        'badge': 'एआई संचालित',
    },
}

def tr(text):
    target = lang_map[st.session_state.lang]['code']
    if target == 'en':
        return str(text)
    try:
        return GoogleTranslator(source='auto', target=target).translate(str(text))
    except Exception:
        return str(text)

t = translations[st.session_state.lang]

# ================= STYLE =================
st.markdown("""
<style>
/* ---------- GLOBAL ---------- */
.stApp {
    background:
        radial-gradient(1200px 600px at 10% -10%, #d7f3df 0%, transparent 60%),
        radial-gradient(900px 500px at 100% 0%, #e6efff 0%, transparent 55%),
        linear-gradient(180deg, #f6fbf7 0%, #f3f7fb 100%);
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: #0f172a;
}
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1200px; }

/* ---------- HERO ---------- */
.hero {
    position: relative;
    background: linear-gradient(135deg, #ffffff 0%, #f7fffb 100%);
    border: 1px solid rgba(34,197,94,0.15);
    border-radius: 22px;
    padding: 30px 34px;
    margin-bottom: 22px;
    box-shadow: 0 18px 50px -25px rgba(16,185,129,0.35);
    overflow: hidden;
}
.hero::before {
    content:"";
    position:absolute; right:-60px; top:-60px;
    width:220px; height:220px; border-radius:50%;
    background: radial-gradient(circle, rgba(34,197,94,0.18), transparent 70%);
}
.hero-badge {
    display:inline-flex; align-items:center; gap:6px;
    background: rgba(34,197,94,0.12);
    color:#15803d;
    font-size:12px; font-weight:600;
    padding: 5px 12px; border-radius: 999px;
    margin-bottom: 10px;
    letter-spacing: .3px;
}
.hero h1 {
    font-size: 38px;
    font-weight: 800;
    margin: 0 0 8px 0;
    background: linear-gradient(135deg, #0f172a 0%, #16a34a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
}
.hero p {
    color:#475569; font-size:15px; margin:0; max-width: 640px;
}

/* ---------- PANEL CARDS ---------- */
.panel {
    background: white;
    border: 1px solid #eef2f7;
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 8px 30px -18px rgba(15,23,42,0.18);
    margin-bottom: 16px;
}
.panel-header {
    display:flex; align-items:center; gap:10px;
    font-size: 13px; font-weight: 700;
    color:#16a34a;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
}
.panel-header .dot {
    width:8px; height:8px; border-radius:50%;
    background:#22c55e;
    box-shadow: 0 0 0 4px rgba(34,197,94,0.18);
}

/* ---------- UPLOADER ---------- */
[data-testid="stFileUploader"] {
    border: 2px dashed #86efac !important;
    background: linear-gradient(180deg,#f7fff9,#ffffff);
    border-radius: 14px;
    padding: 14px;
    transition: all .2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color:#22c55e !important;
    background:#f0fdf4;
}
[data-testid="stFileUploader"] section { padding: 8px; }
[data-testid="stFileUploader"] small { color:#64748b; }

/* ---------- BUTTON ---------- */
.stButton > button {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 15px;
    border: none;
    width: 100%;
    box-shadow: 0 10px 25px -10px rgba(22,163,74,0.55);
    transition: all .2s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 30px -12px rgba(22,163,74,0.6);
    filter: brightness(1.05);
}
.stButton > button:active { transform: translateY(0); }

/* ---------- IMAGE PREVIEW ---------- */
[data-testid="stImage"] img {
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 30px -15px rgba(0,0,0,0.25);
}

/* ---------- RESULT ---------- */
.report-card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    border: 1px solid #eef2f7;
    box-shadow: 0 12px 40px -20px rgba(15,23,42,0.2);
}
.report-title {
    display:flex; align-items:center; gap:10px;
    font-size: 18px; font-weight: 800; color:#0f172a;
    margin-bottom: 6px;
}
.report-sub {
    color:#64748b; font-size:13px; margin-bottom:18px;
}
.section {
    margin-top: 14px;
    padding: 14px 16px;
    border-radius: 12px;
    background: linear-gradient(180deg, #f8fafc, #ffffff);
    border: 1px solid #eef2f7;
}
.section-title {
    font-size: 12px; font-weight: 700;
    color: #16a34a;
    text-transform: uppercase; letter-spacing: 1px;
    margin-bottom: 8px;
}
.section-value {
    font-size: 15px; font-weight: 600; color:#0f172a;
}
.bullet {
    display:flex; align-items:flex-start; gap:10px;
    padding:7px 0; font-size:14px; color:#1f2937;
}
.bullet .pin {
    width:8px; height:8px; border-radius:50%;
    background: linear-gradient(135deg,#22c55e,#16a34a);
    margin-top:7px; flex-shrink:0;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.15);
}

/* ---------- EMPTY STATE ---------- */
.empty {
    text-align:center;
    padding: 50px 24px;
    border: 2px dashed #e2e8f0;
    border-radius: 16px;
    background: #fafafa;
    color:#64748b;
}
.empty .icon {
    font-size: 44px; margin-bottom: 10px;
}

/* ---------- LANG SELECT ---------- */
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
    border: 1px solid #e5e7eb !important;
    background: white !important;
    box-shadow: 0 4px 14px -8px rgba(0,0,0,0.15);
}

/* ---------- SPINNER ---------- */
.stSpinner > div { color:#16a34a !important; }
</style>
""", unsafe_allow_html=True)

# ================= TOP BAR =================
top_l, top_r = st.columns([8, 2])
with top_r:
    selected = st.selectbox(
        "lang",
        options=list(lang_map.keys()),
        index=list(lang_map.keys()).index(st.session_state.lang),
        format_func=lambda x: lang_map[x]['flag'],
        label_visibility="collapsed",
    )
    st.session_state.lang = selected

# ================= HERO =================
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">🌿 {t['badge']}</div>
    <h1>{t['title']}</h1>
    <p>{t['desc']}</p>
</div>
""", unsafe_allow_html=True)

api_url = 'http://leaf-diseases-detect.vercel.app'

# ================= MAIN =================
left, right = st.columns([1, 1.3], gap="large")

with left:
    st.markdown(f"""
    <div class="panel-header"><span class="dot"></span>{t['upload_section']}</div>
    """, unsafe_allow_html=True)

    file = st.file_uploader(t['upload'], type=['jpg', 'jpeg', 'png'], label_visibility="visible")

    if file:
        st.image(file, caption=t['preview'], use_container_width=True)
        detect_clicked = st.button(t['detect'])
    else:
        detect_clicked = False

if r is not None and r.status_code == 200:
    result = r.json()

    st.markdown("""
    <div class="report-card">
        <div class="report-title">📊 Detection Report</div>
        <div class="report-sub">Detailed AI analysis of your uploaded leaf</div>
    """, unsafe_allow_html=True)

    for k, v in result.items():

        # ===== SOLUTION SPECIAL BLOCK =====
        if "solution" in k.lower() or "recommend" in k.lower():

            st.markdown(f"""
            <div style="
                background: #ecfdf5;
                border-left: 5px solid #22c55e;
                border-radius: 12px;
                padding: 14px 16px;
                margin: 12px 0;
            ">
                <div style="
                    font-size: 12px;
                    font-weight: 800;
                    color: #15803d;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    margin-bottom: 8px;
                ">
                    🧪 {tr(k)}
                </div>

                <div style="
                    font-size: 14px;
                    font-weight: 600;
                    color: #064e3b;
                    line-height: 1.5;
                ">
                    {tr(v)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ===== NORMAL BLOCK =====
        else:
            st.markdown(f"""
            <div class="section">
                <div class="section-title">{tr(k)}</div>
            """, unsafe_allow_html=True)

            if isinstance(v, list):
                for item in v:
                    st.markdown(f"""
                    <div class="bullet">
                        <span class="pin"></span>
                        <span>{tr(item)}</span>
                    </div>
                    """, unsafe_allow_html=True)

            elif isinstance(v, dict):
                for ik, iv in v.items():
                    st.markdown(f"""
                    <div class="bullet">
                        <span class="pin"></span>
                        <span><b>{tr(ik)}:</b> {tr(iv)}</span>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="section-value">{tr(v)}</div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
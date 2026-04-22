import streamlit as st
import requests
from deep_translator import GoogleTranslator

st.set_page_config(page_title='Leaf Disease Detection', layout='wide')

# ================= LANGUAGE =================
if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

lang_map = {
    'English': {'code': 'en', 'flag': '🇬🇧 English'},
    'বাংলা': {'code': 'bn', 'flag': '🇧🇩 বাংলা'},
    'हिन्दी': {'code': 'hi', 'flag': '🇮🇳 हिन्दी'}
}

translations = {
    'English': {
        'title': 'Leaf Disease Detection',
        'desc': 'Upload a leaf image and detect diseases instantly.',
        'upload': 'Upload Leaf Image',
        'detect': '🔍 Detect Disease',
        'preview': 'Preview',
        'loading': 'Analyzing image...'
    },
    'বাংলা': {
        'title': 'পাতার রোগ শনাক্তকরণ',
        'desc': 'পাতার ছবি আপলোড করুন এবং সাথে সাথে রোগ শনাক্ত করুন।',
        'upload': 'পাতার ছবি আপলোড করুন',
        'detect': '🔍 পরীক্ষা করুন',
        'preview': 'প্রিভিউ',
        'loading': 'ছবি বিশ্লেষণ করা হচ্ছে...'
    },
    'हिन्दी': {
        'title': 'पत्ती रोग पहचान',
        'desc': 'पत्ती की फोटो अपलोड करें और तुरंत रोग पहचानें।',
        'upload': 'पत्ती की फोटो अपलोड करें',
        'detect': '🔍 जांच करें',
        'preview': 'पूर्वावलोकन',
        'loading': 'छवि का विश्लेषण हो रहा है...'
    }
}

def tr(text):
    target = lang_map[st.session_state.lang]['code']
    if target == 'en':
        return str(text)
    try:
        return GoogleTranslator(source='auto', target=target).translate(str(text))
    except:
        return str(text)

t = translations[st.session_state.lang]

# ================= STYLE =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(120deg, #eef7ee, #f0f7ff);
}

/* Main Card */
.card {
    background: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Title */
h1 {
    text-align: center;
    font-size: 38px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: gray;
    font-size: 16px;
}

/* Upload box */
[data-testid="stFileUploader"] {
    border: 2px dashed #4CAF50;
    padding: 18px;
    border-radius: 14px;
    background: #f9fff9;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #43a047, #66bb6a);
    color: white;
    padding: 12px;
    border-radius: 12px;
    font-weight: 600;
}

/* Result blocks */
.result-box {
    background: #ffffff;
    border-left: 5px solid #4CAF50;
    padding: 15px 18px;
    margin-bottom: 12px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.result-title {
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
}

.result-value {
    font-size: 16px;
    font-weight: 600;
    color: #222;
}

/* top bar */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# ================= TOP BAR (LANG DROPDOWN) =================
col1, col2 = st.columns([8,2])

with col1:
    pass

with col2:
    selected = st.selectbox(
        "",
        options=list(lang_map.keys()),
        index=list(lang_map.keys()).index(st.session_state.lang),
        format_func=lambda x: lang_map[x]['flag']
    )
    st.session_state.lang = selected

# ================= HEADER =================
st.markdown(f"""
<div class="card">
    <h1>{t['title']}</h1>
    <p class="subtitle">{t['desc']}</p>
</div>
""", unsafe_allow_html=True)

api_url = 'http://leaf-diseases-detect.vercel.app'

# ================= MAIN =================
left, right = st.columns([1,2])

with left:
    st.markdown("### 📤 Upload Image")
    file = st.file_uploader(t['upload'], type=['jpg','jpeg','png'])

    if file:
        st.image(file, caption=t['preview'], use_container_width=True)

with right:
    st.markdown("### 🧠 Analysis")

    if file:
        if st.button(t['detect'], use_container_width=True):
            with st.spinner(t['loading']):
                files = {'file': (file.name, file.getvalue(), file.type)}
                r = requests.post(f'{api_url}/disease-detection-file', files=files)

                if r.status_code == 200:
                    result = r.json()

                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    st.markdown("## 🧠 AI Diagnosis Report")

# ================= SUMMARY =================
st.markdown(f"""
<div style="
background:white;
padding:20px;
border-radius:16px;
box-shadow:0 6px 20px rgba(0,0,0,0.06);
margin-bottom:15px;
border-left:6px solid #4CAF50;
">
    <h3 style="margin-bottom:5px;">{tr(result.get('disease_name','Unknown'))}</h3>
    <p style="color:gray;margin:0;">
        Disease Detected: <b>{result.get('disease_detected')}</b>
    </p>
    <p style="margin-top:8px;">
        Confidence: <b style="color:#2e7d32;">{result.get('confidence')}%</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ================= INFO GRID =================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧬 Disease Type")
    st.markdown(f"""
    <div style="background:#f8fafc;padding:14px;border-radius:12px;">
        <b>{tr(result.get('disease_type'))}</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### ⚠️ Severity")
    st.markdown(f"""
    <div style="background:#fff3e0;padding:14px;border-radius:12px;">
        <b>{tr(result.get('severity'))}</b>
    </div>
    """, unsafe_allow_html=True)

# ================= SYMPTOMS =================
st.markdown("### 🌿 Symptoms")

symptoms = result.get("symptoms", [])
if symptoms:
    cols = st.columns(2)
    for i, s in enumerate(symptoms):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="
                background:#e8f5e9;
                padding:10px;
                border-radius:10px;
                margin-bottom:8px;
                font-size:14px;
            ">
            🌱 {tr(s)}
            </div>
            """, unsafe_allow_html=True)

# ================= CAUSES =================
st.markdown("### ⚠️ Possible Causes")

causes = result.get("possible_causes", [])
for c in causes:
    st.markdown(f"""
    <div style="
        background:#f5f5f5;
        padding:12px;
        border-radius:10px;
        margin-bottom:8px;
    ">
    • {tr(c)}
    </div>
    """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error("API Error")
    else:
        st.info("Upload a leaf image to start detection")
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
    background: linear-gradient(135deg, #eef7ee, #f5f9ff);
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER CARD */
.card {
    background: white;
    padding: 22px 26px;
    border-radius: 18px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.06);
    margin-bottom: 18px;
}

/* TITLE */
h1 {
    text-align: center;
    font-size: 34px;
    margin-bottom: 4px;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 15px;
}

/* LAYOUT CARDS */
.block-container {
    padding-top: 1rem;
}

/* UPLOAD BOX */
[data-testid="stFileUploader"] {
    border: 2px dashed #4CAF50;
    padding: 16px;
    border-radius: 14px;
    background: #f7fff7;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    padding: 10px 16px;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(34,197,94,0.3);
}

/* RESULT GRID STYLE */
.result-box {
    background: white;
    padding: 14px 16px;
    border-radius: 14px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.05);
    border: 1px solid #eef2f7;
    margin-bottom: 10px;
}

.result-title {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 4px;
}

.result-value {
    font-size: 15px;
    font-weight: 600;
    color: #111827;
}

/* TOP LANGUAGE DROPDOWN FLOAT STYLE */
.css-1wa3eu0 {
    border-radius: 10px !important;
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
    st.markdown("### 🧠 Analysis Panel")

    if file:

        if st.button(t['detect'], use_container_width=True):

            with st.spinner(t['loading']):

                files = {'file': (file.name, file.getvalue(), file.type)}
                r = requests.post(f'{api_url}/disease-detection-file', files=files)

                if r.status_code == 200:
                    result = r.json()

                    st.markdown("""
                    <div class="card">
                        <h3 style="margin-bottom:15px;">📊 Detection Report</h3>
                    """, unsafe_allow_html=True)

                    for k, v in result.items():

                        # SECTION CARD
                        st.markdown(f"""
                        <div style="
                            background:white;
                            padding:16px;
                            border-radius:14px;
                            margin-bottom:12px;
                            box-shadow:0 3px 15px rgba(0,0,0,0.06);
                            border-left:4px solid #22c55e;
                        ">
                            <div style="font-size:13px;color:#6b7280;margin-bottom:6px;">
                                {tr(k)}
                            </div>
                        """, unsafe_allow_html=True)

                        # LIST TYPE
                        if isinstance(v, list):
                            for item in v:
                                st.markdown(f"""
                                <div style="
                                    padding:8px 10px;
                                    background:#f8fafc;
                                    border-radius:10px;
                                    margin-bottom:6px;
                                    font-size:14px;
                                    font-weight:500;
                                ">
                                    • {tr(item)}
                                </div>
                                """, unsafe_allow_html=True)

                        # SINGLE VALUE
                        else:
                            st.markdown(f"""
                            <div style="
                                font-size:16px;
                                font-weight:600;
                                color:#111827;
                                padding:6px 0;
                            ">
                                {tr(v)}
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                else:
                    st.error("API Error")

    else:
        st.info("Upload a leaf image to start detection")
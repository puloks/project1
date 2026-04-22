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

/* HEADER */
.header {
    text-align: center;
    padding: 20px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.06);
}

/* CARD */
.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* RESULT GRID */
.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

/* compact box */
.box {
    background: #f9fff9;
    padding: 12px 14px;
    border-radius: 12px;
    border-left: 4px solid #4CAF50;
}

/* title */
.title {
    font-size: 13px;
    color: #666;
}

/* value */
.value {
    font-size: 15px;
    font-weight: 600;
    color: #222;
}

/* upload */
[data-testid="stFileUploader"] {
    border: 2px dashed #4CAF50;
    padding: 14px;
    border-radius: 12px;
    background: #f9fff9;
}

/* button */
.stButton > button {
    background: linear-gradient(135deg, #43a047, #66bb6a);
    color: white;
    padding: 12px;
    border-radius: 12px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ================= LANG DROPDOWN =================
col1, col2 = st.columns([8,2])

with col2:
    st.session_state.lang = st.selectbox(
        "",
        list(lang_map.keys()),
        index=list(lang_map.keys()).index(st.session_state.lang),
        format_func=lambda x: lang_map[x]['flag']
    )

# ================= HEADER =================
st.markdown(f"""
<div class="header">
    <h2>{t['title']}</h2>
    <p>{t['desc']}</p>
</div>
""", unsafe_allow_html=True)

api_url = 'http://leaf-diseases-detect.vercel.app'

# ================= MAIN =================
left, right = st.columns([1,2])

with left:
    st.markdown("### 📤 Upload")
    file = st.file_uploader(t['upload'], type=['jpg','jpeg','png'])

    if file:
        st.image(file, use_container_width=True)

with right:
    st.markdown("### 📊 Result Dashboard")

    if file:
        if st.button(t['detect'], use_container_width=True):
            with st.spinner(t['loading']):
                files = {'file': (file.name, file.getvalue(), file.type)}
                r = requests.post(f'{api_url}/disease-detection-file', files=files)

                if r.status_code == 200:
                    result = r.json()

                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    # 🔥 TOP SUMMARY (first key-value only)
                    keys = list(result.keys())
                    if keys:
                        first_key = keys[0]
                        st.markdown(f"### 🧾 {tr(first_key)}")
                        st.markdown(f"**{tr(result[first_key]) if not isinstance(result[first_key], list) else ', '.join(map(tr, result[first_key]))}**")

                    st.markdown("---")

                    # GRID RESULT
                    st.markdown('<div class="grid">', unsafe_allow_html=True)

                    for k, v in list(result.items())[1:]:
                        if isinstance(v, list):
                            value = ", ".join([tr(i) for i in v[:2]])  # 🔥 limit 2 items only
                        else:
                            value = tr(v)

                        st.markdown(f"""
                        <div class="box">
                            <div class="title">{tr(k)}</div>
                            <div class="value">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error("API Error")
    else:
        st.info("Upload a leaf image to see results")
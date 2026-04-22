import streamlit as st
import requests
from deep_translator import GoogleTranslator

st.set_page_config(page_title='Leaf Disease Detection', layout='wide')

if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

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
    lang_map = {'English': 'en', 'বাংলা': 'bn', 'हिन्दी': 'hi'}
    target = lang_map[st.session_state.lang]
    if target == 'en':
        return str(text)
    try:
        return GoogleTranslator(source='auto', target=target).translate(str(text))
    except:
        return str(text)

t = translations[st.session_state.lang]

# ====== GLOBAL STYLE ======
st.markdown("""
<style>

.stApp {
    background: linear-gradient(120deg, #eef7ee, #f0f7ff);
}

/* Top language buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
}

/* Main card */
.card {
    background: white;
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* Upload box feel */
[data-testid="stFileUploader"] {
    border: 2px dashed #4CAF50;
    padding: 20px;
    border-radius: 15px;
    background: #f9fff9;
}

/* Big gradient button */
.stButton > button {
    background: linear-gradient(135deg, #43a047, #66bb6a);
    color: white;
    padding: 12px 18px;
    font-size: 16px;
    border-radius: 14px;
}

/* Title */
h1 {
    font-size: 40px;
    text-align: center;
    margin-bottom: 10px;
}

/* subtitle */
.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ===== LANGUAGE SWITCH =====
c1, c2, c3 = st.columns(3)
with c1:
    if st.button('English', use_container_width=True):
        st.session_state.lang = 'English'
        st.rerun()
with c2:
    if st.button('বাংলা', use_container_width=True):
        st.session_state.lang = 'বাংলা'
        st.rerun()
with c3:
    if st.button('हिन्दी', use_container_width=True):
        st.session_state.lang = 'हिन्दी'
        st.rerun()

# ===== HERO =====
st.markdown(f"""
<div class="card">
    <h1>{t['title']}</h1>
    <p class="subtitle">{t['desc']}</p>
</div>
""", unsafe_allow_html=True)

api_url = 'http://leaf-diseases-detect.vercel.app'

left, right = st.columns([1, 2])

with left:
    st.markdown("### 📤 Upload")
    file = st.file_uploader(t['upload'], type=['jpg', 'jpeg', 'png'])

    if file:
        st.image(file, caption=t['preview'], use_container_width=True)

with right:
    st.markdown("### 🤖 Detection Result")

    if file:
        if st.button(t['detect'], use_container_width=True):
            with st.spinner(t['loading']):
                files = {'file': (file.name, file.getvalue(), file.type)}
                r = requests.post(f'{api_url}/disease-detection-file', files=files)

                if r.status_code == 200:
                    result = r.json()

                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    for k, v in result.items():
                        if isinstance(v, list):
                            st.markdown(f"**{tr(k)}**")
                            for item in v:
                                st.write("• " + tr(item))
                        else:
                            st.write(f"**{tr(k)}:** {tr(v)}")

                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("API Error")
    else:
        st.info("Upload a leaf image to start detection")